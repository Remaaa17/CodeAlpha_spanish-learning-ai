# 🚀 Quick Start Guide

## Installation (5 minutes)

### 1. Open Terminal/Command Prompt in this directory

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the application
```bash
python app.py
```

### 6. Open your browser
Navigate to: **http://localhost:5000**

## 🎉 That's it! You're ready to go!

---

## Features to Try

### Translation Tool (📝 Tab)
1. Select source language (e.g., English)
2. Select target language (e.g., Spanish)
3. Type or paste text
4. Click "Translate"
5. Try the "Copy" and "Speak" buttons
6. Use the swap button (⇄) to reverse languages

### NLP Chatbot (💬 Tab)
1. Click any quick question button
2. Or type your own question about learning Spanish
3. Watch the AI find the best matching answer using NLP!

Example questions:
- "How do I start learning Spanish?"
- "What are verb conjugations?"
- "Tell me about pronunciation"
- "Difference between ser and estar"
- "Show me common phrases"

---

## How the AI Works

### Translation
- Uses Google Translate API (free)
- Falls back to MyMemory API if needed
- No API key required!

### Chatbot NLP
1. **Tokenization**: Breaks text into words
2. **Stopword Removal**: Removes common words (the, is, a, etc.)
3. **Lemmatization**: Converts words to base form
4. **TF-IDF**: Converts text to numerical vectors
5. **Cosine Similarity**: Finds most similar FAQ
6. **Returns best match**: Shows the answer!

---

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Port 5000 in use
Change port in `app.py`:
```python
app.run(debug=True, port=8000)
```

### NLTK data errors
Run:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## Test Individual Components

### Test Translation
```bash
python translation_service.py
```

### Test Chatbot NLP
```bash
python chatbot_service.py
```

---

## Project Structure
```
spanish-learning-ai/
├── app.py                 # 🚀 Main Flask app (START HERE)
├── translation_service.py # 🌐 Translation API
├── chatbot_service.py     # 🤖 NLP Chatbot
├── static/
│   ├── style.css         # 🎨 Styling
│   └── script.js         # ⚡ Frontend logic
└── templates/
    └── index.html        # 📄 Web interface
```

---

## Need Help?

Check the full README.md for detailed documentation!

**¡Buena suerte!** 🇪🇸
