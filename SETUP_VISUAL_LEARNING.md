# 🚀 Quick Setup Guide - Visual Learning Feature

## Step 1: Install Python Dependencies

```bash
cd spanish-learning-ai
pip install -r requirements.txt
```

**New dependencies installed:**
- opencv-python (video processing)
- ultralytics (YOLO)
- torch & torchvision (deep learning)
- scipy (Hungarian algorithm)
- filterpy (Kalman Filter)

**Time:** ~5-10 minutes (downloading packages)

---

## Step 2: First Run - YOLO Model Download

The YOLOv8 model will auto-download on first use:

```bash
python app.py
```

**Expected console output:**
```
🎥 Initializing Visual Learning Service...
Downloading yolov8n.pt from https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt...
100%|████████████████████████████████| 6.23M/6.23M [00:02<00:00, 2.85MB/s]
✓ YOLO model loaded
✓ Visual Learning Service ready!
```

**Time:** ~1-2 minutes (one-time download, 6MB model)

---

## Step 3: Test Webcam Access

1. Open browser: `http://localhost:5000`
2. Navigate to **"Visual"** tab
3. Click **"Start Webcam"**
4. Allow camera access when prompted
5. Click **"Detect Objects"**

**Troubleshooting:**
- If webcam doesn't work: Try **"Upload Image"** instead
- If slow: Lower confidence threshold or use smaller images

---

## Step 4: Test Object Detection

**Method A - Webcam:**
1. Point camera at common objects (laptop, phone, cup, etc.)
2. Click "Detect Objects"
3. Watch bounding boxes appear with Spanish translations!

**Method B - Image Upload:**
1. Click "Upload Image"
2. Select any image with recognizable objects
3. See instant detection + translation

**Expected:**
- Bounding boxes drawn
- Labels: "ID:1 laptop/portátil 0.95"
- Detection panel updates
- Vocabulary grid shows translations

---

## Step 5: Save to Flashcards

1. After detecting objects, click **"Save to Flashcards"**
2. New vocabulary added to database
3. Navigate to **"Flashcards"** tab
4. Click **"Start Practice"**
5. See your detected vocabulary as flashcards!

**Example:**
```
Detected: car, person, bicycle
  ↓
Saved as:
  • car/coche
  • person/persona
  • bicycle/bicicleta
  ↓
Practice in Flashcards tab!
```

---

## Common Issues & Solutions

### Issue 1: YOLO model not downloading
**Solution:**
```python
# Manual download:
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
```

### Issue 2: Webcam not detected
**Solution:**
- Check browser permissions
- Use Chrome/Firefox (better camera support)
- Try "Upload Image" as alternative

### Issue 3: Slow detection
**Solution:**
- Use smaller images (640x480)
- Lower confidence threshold
- Close other apps
- GPU will help if available

### Issue 4: Import errors
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## Performance Optimization

### For Faster Detection:

**1. Use GPU (if available):**
```python
# PyTorch will automatically use CUDA if available
# Check with:
import torch
print(torch.cuda.is_available())
```

**2. Lower Resolution:**
- Resize images to 640x480 before upload
- Webcam set to 640x480 by default

**3. Increase Confidence Threshold:**
- Less detections = faster processing
- Default: 0.5 (50%)
- Try: 0.6 or 0.7 for fewer results

---

## Testing Checklist

- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] "Visual" tab visible
- [ ] Webcam works OR image upload works
- [ ] Objects detected with bounding boxes
- [ ] Spanish translations shown
- [ ] Tracking IDs assigned
- [ ] Vocabulary grid updates
- [ ] "Save to Flashcards" works
- [ ] New flashcards appear in Flashcards tab

---

## Expected Performance

| Hardware | Detection Speed | Recommended |
|----------|----------------|-------------|
| CPU Only | 1-3 FPS | ✓ Basic use |
| GPU (NVIDIA) | 30-100+ FPS | ✓✓ Smooth real-time |
| High-end CPU | 5-10 FPS | ✓ Good experience |

---

## What You Should See

### Console:
```
✓ Enhanced Chatbot initialized with 20 FAQs
✓ Groq API enabled for advanced questions
✓ Database initialized successfully
🎥 Initializing Visual Learning Service...
✓ YOLO model loaded
✓ Visual Learning Service ready!

🇪🇸 Spanish Learning AI Assistant
==================================================
📝 Translation API: ✓
💬 NLP Chatbot: ✓
🃏 Flashcard System: ✓
📊 Quiz System: ✓
📚 Learning Paths: ✓
🎮 Gamification: ✓
🎥 Visual Learning (YOLO + Deep SORT): ✓
==================================================
```

### Browser Visual Tab:
- Video feed with real-time annotations
- Detection panel with object list
- Vocabulary grid with English/Spanish pairs
- Statistics (object count, unique words)
- Control buttons (Start/Stop/Detect/Upload)

---

## Quick Demo Script

**For CodeAlpha presentation:**

1. **Introduction** (30 seconds)
   - "This combines object detection with language learning"
   
2. **Start Webcam** (10 seconds)
   - Click "Start Webcam"
   - Camera activates

3. **Detect Objects** (20 seconds)
   - Point at laptop, phone, cup
   - Click "Detect Objects"
   - Show bounding boxes with Spanish

4. **Show Vocabulary** (10 seconds)
   - Point to vocabulary grid
   - "All detected objects with translations"

5. **Save to Flashcards** (15 seconds)
   - Click "Save to Flashcards"
   - Navigate to Flashcards tab
   - Show new vocabulary cards

6. **Technical Explanation** (30 seconds)
   - "YOLOv8 for detection"
   - "Deep SORT for tracking"
   - "Automatic Spanish translation"
   - "Integrated with flashcard system"

**Total:** ~2 minutes

---

## Dependencies Summary

```txt
# Computer Vision
opencv-python==4.8.1.78
opencv-contrib-python==4.8.1.78

# Object Detection
ultralytics==8.0.232
torch==2.1.1
torchvision==0.16.1

# Tracking
scipy==1.11.4
filterpy==1.4.5

# Core
numpy==1.26.2
Pillow==10.1.0

# Existing
Flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
nltk==3.8.1
scikit-learn==1.3.2
groq==0.4.1
```

---

## File Structure

```
spanish-learning-ai/
├── backend/
│   ├── services/
│   │   ├── deep_sort_tracker.py        [NEW - 350 lines]
│   │   ├── visual_learning_service.py  [NEW - 400 lines]
│   │   └── ... (other services)
│   ├── api/
│   │   ├── visual_learning_routes.py   [NEW - 200 lines]
│   │   └── ... (other routes)
│   └── ...
├── frontend/
│   ├── pages/
│   │   └── index.html                   [UPDATED - Visual tab added]
│   └── assets/
│       ├── js/
│       │   └── script.js                [UPDATED - 300+ lines added]
│       └── css/
│           └── style.css                [UPDATED - 250+ lines added]
├── requirements.txt                     [UPDATED - CV dependencies]
├── app.py                               [UPDATED - Visual routes]
└── VISUAL_LEARNING_TASK4_COMPLETE.md    [NEW - Documentation]
```

---

## Success Criteria

✅ **Setup complete when:**
- Server starts without errors
- Visual tab loads
- Webcam or image upload works
- Objects detected with bounding boxes
- Spanish translations appear
- Tracking IDs assigned
- Vocabulary can be saved to flashcards

---

## Need Help?

**Check these files:**
1. `VISUAL_LEARNING_TASK4_COMPLETE.md` - Full technical docs
2. `requirements.txt` - All dependencies
3. Console output - Error messages
4. Browser console (F12) - JavaScript errors

**Common fixes:**
- Restart server: `Ctrl+C` then `python app.py`
- Clear browser cache: `Ctrl+Shift+Delete`
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`
- Check Python version: `python --version` (3.8+ required)

---

## Ready to Go!

Once setup is complete:
1. Server running on `http://localhost:5000`
2. Visual tab accessible
3. Webcam or upload ready
4. Start learning Spanish through object detection!

**Enjoy your AI-powered Visual Spanish Learning experience! 🎥📚🇪🇸**
