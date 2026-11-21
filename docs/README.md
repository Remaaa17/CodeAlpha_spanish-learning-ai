# 🇪🇸 Spanish Learning AI Assistant

An AI-powered web application to support Spanish learning with two core features:

1. **Translation Tool** - Multi-language translator using Google Translate API
2. **NLP Chatbot** - Intelligent FAQ chatbot using NLTK and scikit-learn

## 🎯 Project Overview

This project demonstrates practical application of AI/ML techniques for language learning:

- **Translation Service**: Real-time translation using Google Translate API with fallback to MyMemory API
- **NLP Processing**: Text preprocessing with NLTK (tokenization, lemmatization, stopword removal)
- **Machine Learning**: TF-IDF vectorization and cosine similarity for intent matching
- **Web Framework**: Flask backend with RESTful API
- **Frontend**: Clean, responsive HTML/CSS/JavaScript interface

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **NLTK** - Natural Language Processing
- **scikit-learn** - TF-IDF vectorization and cosine similarity
- **googletrans** - Translation API client
- **NumPy** - Numerical computing

### Frontend
- HTML5, CSS3, JavaScript
- Responsive design
- Web Speech API for text-to-speech

## 📋 Features

### Translation Tool
- ✅ Multi-language support (English, Spanish, French, German, Italian, Portuguese)
- ✅ Real-time translation using Google Translate API
- ✅ Fallback to MyMemory API for reliability
- ✅ Language swap functionality
- ✅ Copy to clipboard
- ✅ Text-to-speech pronunciation
- ✅ Clean, intuitive interface

### NLP Chatbot
- ✅ 15+ comprehensive Spanish learning FAQs
- ✅ NLP-powered question matching using:
  - Tokenization
  - Stopword removal
  - Lemmatization
  - TF-IDF vectorization
  - Cosine similarity matching
- ✅ Topics covered:
  - Getting started with Spanish
  - Grammar and verb conjugations
  - Pronunciation guides
  - Ser vs Estar
  - Common phrases
  - Learning resources
  - Vocabulary tips
  - Days, months, numbers
  - And more!
- ✅ Quick question buttons
- ✅ Natural conversation interface

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd spanish-learning-ai
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
The application will automatically download required NLTK data on first run, but you can manually download it:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📁 Project Structure

```
spanish-learning-ai/
├── app.py                      # Flask application (main entry point)
├── translation_service.py      # Translation API integration
├── chatbot_service.py          # NLP chatbot with TF-IDF & cosine similarity
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── static/
│   ├── style.css              # CSS styling
│   └── script.js              # Frontend JavaScript
└── templates/
    └── index.html             # HTML template
```

## 🔧 How It Works

### Translation Service (`translation_service.py`)

1. Uses `googletrans` library as primary translation method
2. Falls back to MyMemory API if googletrans fails
3. Supports language detection
4. No API key required (uses free tier)

```python
def translate_text(text, source_lang='en', target_lang='es'):
    # Uses Google Translate API via googletrans library
    result = translator.translate(text, src=source_lang, dest=target_lang)
    return result.text
```

### NLP Chatbot (`chatbot_service.py`)

**Architecture:**
1. **Preprocessing**: 
   - Tokenization using NLTK
   - Stopword removal
   - Lemmatization
   
2. **Vectorization**:
   - TF-IDF (Term Frequency-Inverse Document Frequency)
   - Creates numerical vectors from text

3. **Similarity Matching**:
   - Cosine similarity between user query and FAQ database
   - Returns best matching answer

```python
# Key NLP Pipeline
user_vector = vectorizer.transform([user_message])
similarities = cosine_similarity(user_vector, question_vectors)
best_match = np.argmax(similarities)
```

**Why TF-IDF + Cosine Similarity?**
- Lightweight and fast
- No need for training data
- Works well for FAQ matching
- Computationally efficient
- Suitable for small to medium datasets

## 📊 API Endpoints

### Translation API
```
POST /api/translate
Body: {
    "text": "Hello",
    "source_lang": "en",
    "target_lang": "es"
}
Response: {
    "success": true,
    "translated_text": "Hola",
    "source_lang": "en",
    "target_lang": "es"
}
```

### Chatbot API
```
POST /api/chat
Body: {
    "message": "How do I start learning Spanish?"
}
Response: {
    "success": true,
    "response": "¡Bienvenido! To start learning Spanish...",
    "user_message": "How do I start learning Spanish?"
}
```

### Get All FAQs
```
GET /api/faqs
Response: {
    "success": true,
    "faqs": [...]
}
```

## 🧪 Testing

### Test Translation Service
```bash
python translation_service.py
```

### Test Chatbot
```bash
python chatbot_service.py
```

## 🎨 Customization

### Adding More FAQs
Edit `chatbot_service.py` in the `_load_faqs()` method:

```python
{
    "question": "Your question here?",
    "answer": "Your detailed answer...",
    "keywords": ["keyword1", "keyword2"]
}
```

### Adjusting Similarity Threshold
In `chatbot_service.py`, modify the threshold in `get_response()`:

```python
if best_score > 0.15:  # Change this value (0.0 to 1.0)
    return self.answers[best_match_idx]
```

Lower threshold = More lenient matching
Higher threshold = Stricter matching

### Using Different Translation APIs

**Option 1: Google Cloud Translation API** (requires API key)
```python
from google.cloud import translate_v2 as translate
```

**Option 2: Microsoft Translator** (requires subscription key)
```python
import requests
# See translation_service.py for commented implementation
```

## 📈 Future Enhancements

- [ ] Add more Spanish learning content
- [ ] Implement conversation history
- [ ] Add flashcard system
- [ ] Progress tracking
- [ ] Voice input for translation
- [ ] Deploy to cloud (Heroku, AWS, Azure)
- [ ] Add user authentication
- [ ] Save favorite phrases
- [ ] Integrate with Spanish dictionary API
- [ ] Add quiz functionality

## 🤖 AI/ML Concepts Demonstrated

1. **Natural Language Processing (NLP)**
   - Text tokenization
   - Stopword removal
   - Lemmatization
   - Text preprocessing

2. **Feature Engineering**
   - TF-IDF vectorization
   - Text to numerical representation

3. **Similarity Metrics**
   - Cosine similarity
   - Vector space models

4. **API Integration**
   - Translation APIs
   - RESTful API design

5. **Web Development**
   - Backend with Flask
   - Frontend integration
   - Asynchronous communication

## 🎓 Learning Resources

To understand the NLP concepts used:
- [NLTK Documentation](https://www.nltk.org/)
- [TF-IDF Explained](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [scikit-learn Documentation](https://scikit-learn.org/)

## 🐛 Troubleshooting

### Issue: NLTK data not found
**Solution**: Run the download command manually
```python
python -c "import nltk; nltk.download('all')"
```

### Issue: googletrans errors
**Solution**: The app will automatically fall back to MyMemory API. If issues persist, check your internet connection.

### Issue: Port 5000 already in use
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 📝 License

This project is created for educational purposes as part of an AI internship task.

## 👨‍💻 Author

Created as an AI internship project demonstrating:
- Python programming
- NLP techniques
- API integration
- Web development
- Machine learning concepts

---

**¡Buena suerte con tu español!** (Good luck with your Spanish!)

For questions or improvements, feel free to reach out!
