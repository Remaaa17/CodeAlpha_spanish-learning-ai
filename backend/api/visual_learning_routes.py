"""
Visual Learning API Routes
Real-time object detection with Spanish translation
"""

from flask import Blueprint, request, jsonify, Response
import cv2
import numpy as np
import base64
from backend.services.visual_learning_service import get_visual_learning_service

visual_bp = Blueprint('visual', __name__, url_prefix='/api/visual')

# Get service instance
visual_service = None

def get_service():
    """Lazy load visual learning service"""
    global visual_service
    if visual_service is None:
        visual_service = get_visual_learning_service()
    return visual_service


@visual_bp.route('/detect', methods=['POST'])
def detect_objects():
    """
    Detect objects in uploaded frame
    Expects base64 encoded image
    """
    try:
        data = request.json
        image_data = data.get('image')
        confidence = data.get('confidence', 0.5)
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        img_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image'}), 400
        
        # Detect objects
        service = get_service()
        annotated_frame, detections = service.detect_frame(frame, confidence)
        
        # Encode result frame
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        result_image = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/jpeg;base64,{result_image}',
            'detections': detections,
            'count': len(detections)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@visual_bp.route('/webcam/status', methods=['GET'])
def webcam_status():
    """Check if webcam is available"""
    try:
        cap = cv2.VideoCapture(0)
        is_available = cap.isOpened()
        if is_available:
            cap.release()
        
        return jsonify({
            'success': True,
            'available': is_available
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'available': False,
            'error': str(e)
        })


@visual_bp.route('/vocabulary/summary', methods=['GET'])
def vocabulary_summary():
    """Get vocabulary learning summary from detected objects"""
    try:
        service = get_service()
        summary = service.get_vocabulary_summary()
        
        return jsonify({
            'success': True,
            'vocabulary': summary,
            'count': len(summary)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@visual_bp.route('/vocabulary/save', methods=['POST'])
def save_vocabulary():
    """Save detected vocabulary to flashcards"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        
        service = get_service()
        added_count = service.save_vocabulary_to_flashcards(user_id)
        
        return jsonify({
            'success': True,
            'added_count': added_count,
            'message': f'Added {added_count} new flashcards from detected objects'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@visual_bp.route('/session/stats', methods=['GET'])
def session_stats():
    """Get current session statistics"""
    try:
        service = get_service()
        stats = service.get_session_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@visual_bp.route('/session/reset', methods=['POST'])
def reset_session():
    """Reset tracking session"""
    try:
        service = get_service()
        service.reset_session()
        
        return jsonify({
            'success': True,
            'message': 'Session reset successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@visual_bp.route('/video/file', methods=['POST'])
def process_video_file():
    """
    Process uploaded video file
    Returns processed video with detections
    """
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        
        # Save temporarily
        temp_path = 'temp_video.mp4'
        video_file.save(temp_path)
        
        # Process video
        service = get_service()
        cap = cv2.VideoCapture(temp_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Process frames
        frames_processed = 0
        all_detections = []
        
        while cap.isOpened() and frames_processed < 100:  # Limit to 100 frames
            ret, frame = cap.read()
            if not ret:
                break
            
            annotated_frame, detections = service.detect_frame(frame)
            all_detections.extend(detections)
            frames_processed += 1
        
        cap.release()
        
        return jsonify({
            'success': True,
            'frames_processed': frames_processed,
            'total_detections': len(all_detections),
            'unique_objects': len(set(d['english'] for d in all_detections)),
            'vocabulary': service.get_vocabulary_summary()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@visual_bp.route('/models/info', methods=['GET'])
def model_info():
    """Get information about loaded models"""
    try:
        service = get_service()
        
        return jsonify({
            'success': True,
            'model': 'YOLOv8 Nano',
            'tracker': 'Deep SORT',
            'framework': 'Ultralytics',
            'features': [
                'Real-time object detection',
                'Multi-object tracking',
                'Spanish translation',
                'Vocabulary learning',
                'Flashcard integration'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
