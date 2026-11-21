"""
Visual Spanish Learning Service
Combines object detection with Spanish translation
"""

import cv2
import numpy as np
from ultralytics import YOLO
from backend.services.deep_sort_tracker import DeepSORTTracker
from backend.services.translation_service import translate_text
from backend.models.database import get_db
import time
from datetime import datetime


class VisualLearningService:
    """
    Real-time object detection with Spanish translation
    """
    
    def __init__(self):
        """Initialize YOLO model and Deep SORT tracker"""
        print("🎥 Initializing Visual Learning Service...")
        
        # Load YOLOv8 model (pre-trained on COCO dataset)
        try:
            self.model = YOLO('yolov8n.pt')  # Nano model for speed
            print("✓ YOLO model loaded")
        except Exception as e:
            print(f"✗ Error loading YOLO: {e}")
            self.model = None
        
        # Initialize Deep SORT tracker
        self.tracker = DeepSORTTracker(
            max_age=30,      # Keep track for 30 frames without detection
            min_hits=3,      # Minimum 3 detections to confirm track
            iou_threshold=0.3  # IOU threshold for matching
        )
        
        # Cache for translations (avoid repeated API calls)
        self.translation_cache = {}
        
        # Track detected objects for vocabulary learning
        self.detected_objects = {}  # {track_id: {label, spanish, count, first_seen}}
        
        # Colors for bounding boxes (BGR format)
        self.colors = self._generate_colors(80)  # COCO has 80 classes
        
        print("✓ Visual Learning Service ready!")
    
    def _generate_colors(self, num_colors):
        """Generate distinct colors for bounding boxes"""
        np.random.seed(42)
        return np.random.randint(0, 255, size=(num_colors, 3), dtype=np.uint8).tolist()
    
    def _translate_to_spanish(self, english_word):
        """
        Translate English word to Spanish with caching
        """
        # Check cache first
        if english_word in self.translation_cache:
            return self.translation_cache[english_word]
        
        # Translate
        try:
            spanish_word = translate_text(
                text=english_word,
                source_lang='en',
                target_lang='es'
            )
            
            # Cache the translation
            self.translation_cache[english_word] = spanish_word
            
            return spanish_word
        except:
            return english_word  # Fallback to English
    
    def detect_frame(self, frame, confidence_threshold=0.5):
        """
        Detect objects in a single frame
        
        Args:
            frame: BGR image from OpenCV
            confidence_threshold: Minimum confidence for detection
        
        Returns:
            annotated_frame: Frame with bounding boxes and labels
            detections: List of detected objects with Spanish translations
        """
        if self.model is None:
            return frame, []
        
        # Run YOLO detection
        results = self.model(frame, conf=confidence_threshold, verbose=False)
        
        # Extract detections
        detections = []
        boxes_for_tracking = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Get confidence and class
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                # Get class name
                class_name = result.names[cls]
                
                # Add to detections for tracking
                boxes_for_tracking.append([x1, y1, x2, y2])
                
                detections.append({
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': conf,
                    'class_id': cls,
                    'class_name': class_name
                })
        
        # Update tracker
        tracked_objects = []
        if len(boxes_for_tracking) > 0:
            tracked_objects = self.tracker.update(np.array(boxes_for_tracking))
        
        # Annotate frame with tracking IDs and Spanish translations
        annotated_frame = frame.copy()
        detection_results = []
        
        for i, track in enumerate(tracked_objects):
            x1, y1, x2, y2, track_id = track
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            track_id = int(track_id)
            
            # Get corresponding detection
            if i < len(detections):
                det = detections[i]
                class_name = det['class_name']
                confidence = det['confidence']
                class_id = det['class_id']
                
                # Translate to Spanish
                spanish_name = self._translate_to_spanish(class_name)
                
                # Update detected objects tracker
                if track_id not in self.detected_objects:
                    self.detected_objects[track_id] = {
                        'english': class_name,
                        'spanish': spanish_name,
                        'count': 1,
                        'first_seen': datetime.now(),
                        'class_id': class_id
                    }
                else:
                    self.detected_objects[track_id]['count'] += 1
                
                # Choose color based on class
                color = self.colors[class_id % len(self.colors)]
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Prepare label with ID and translation
                label = f"ID:{track_id} {class_name}/{spanish_name} {confidence:.2f}"
                
                # Draw label background
                (label_width, label_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                )
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1 - label_height - 10),
                    (x1 + label_width, y1),
                    color,
                    -1
                )
                
                # Draw label text
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )
                
                detection_results.append({
                    'track_id': track_id,
                    'english': class_name,
                    'spanish': spanish_name,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })
        
        return annotated_frame, detection_results
    
    def get_vocabulary_summary(self):
        """
        Get summary of detected objects for vocabulary learning
        
        Returns:
            List of unique objects with translations and detection counts
        """
        summary = []
        
        # Group by English word
        word_stats = {}
        for track_id, data in self.detected_objects.items():
            english = data['english']
            if english not in word_stats:
                word_stats[english] = {
                    'english': english,
                    'spanish': data['spanish'],
                    'total_detections': 0,
                    'unique_tracks': 0
                }
            word_stats[english]['total_detections'] += data['count']
            word_stats[english]['unique_tracks'] += 1
        
        # Convert to list and sort by detections
        summary = list(word_stats.values())
        summary.sort(key=lambda x: x['total_detections'], reverse=True)
        
        return summary
    
    def save_vocabulary_to_flashcards(self, user_id=1):
        """
        Save detected vocabulary to flashcard database
        
        Returns:
            Number of flashcards added
        """
        conn = get_db()
        cursor = conn.cursor()
        
        added_count = 0
        
        for english, data in self._get_unique_vocabulary().items():
            spanish = data['spanish']
            
            # Check if already exists
            cursor.execute('''
                SELECT id FROM flashcards 
                WHERE spanish_word = ? AND english_word = ?
            ''', (spanish, english))
            
            if cursor.fetchone() is None:
                # Add new flashcard
                cursor.execute('''
                    INSERT INTO flashcards 
                    (spanish_word, english_word, category, difficulty, example_sentence)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    spanish,
                    english,
                    'visual_learning',
                    'easy',
                    f'Detected via camera: {english} = {spanish}'
                ))
                added_count += 1
        
        conn.commit()
        conn.close()
        
        return added_count
    
    def _get_unique_vocabulary(self):
        """Get unique vocabulary from detected objects"""
        vocab = {}
        for track_id, data in self.detected_objects.items():
            english = data['english']
            if english not in vocab:
                vocab[english] = {
                    'spanish': data['spanish'],
                    'count': data['count']
                }
        return vocab
    
    def reset_session(self):
        """Reset tracking session"""
        self.detected_objects = {}
        self.tracker.reset()
    
    def get_session_stats(self):
        """Get statistics about current session"""
        return {
            'unique_objects': len(self._get_unique_vocabulary()),
            'total_tracks': len(self.detected_objects),
            'vocabulary': self.get_vocabulary_summary()
        }


# Global service instance
visual_learning_service = None

def get_visual_learning_service():
    """Get or create visual learning service instance"""
    global visual_learning_service
    if visual_learning_service is None:
        visual_learning_service = VisualLearningService()
    return visual_learning_service
