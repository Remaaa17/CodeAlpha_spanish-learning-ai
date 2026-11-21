"""
Spanish Learning Chatbot Service
Uses NLTK for NLP processing and scikit-learn for similarity matching
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Download required NLTK data (only first time)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')

class SpanishLearningChatbot:
    """
    NLP-powered chatbot for Spanish learning FAQs
    Uses TF-IDF and cosine similarity for intent matching
    """
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()
        
        # Load FAQs
        self.faqs = self._load_faqs()
        self.questions = [faq['question'] for faq in self.faqs]
        self.answers = [faq['answer'] for faq in self.faqs]
        
        # Fit vectorizer on questions
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
        
        print(f"✓ Chatbot initialized with {len(self.faqs)} FAQs")
    
    def _load_faqs(self):
        """Load Spanish learning FAQs"""
        return [
            {
                "question": "How do I start learning Spanish?",
                "answer": "¡Bienvenido! To start learning Spanish:\n\n1. Learn the alphabet and pronunciation basics\n2. Master common greetings: Hola (Hello), Buenos días (Good morning)\n3. Study basic vocabulary (numbers, colors, days, foods)\n4. Practice with simple phrases daily\n5. Use apps like Duolingo or this tool!\n6. Watch Spanish TV shows with subtitles\n7. Practice speaking, even if you make mistakes!\n\nConsistency is key. Practice 15-30 minutes daily.",
                "keywords": ["start", "begin", "beginner", "learn spanish", "how to"]
            },
            {
                "question": "What are Spanish verb conjugations?",
                "answer": "Spanish verb conjugations change based on the subject and tense. Here are present tense endings:\n\n**-AR verbs (hablar - to speak):**\n• Yo hablo (I speak)\n• Tú hablas (You speak)\n• Él/Ella habla (He/She speaks)\n• Nosotros hablamos (We speak)\n• Ellos hablan (They speak)\n\n**-ER verbs (comer - to eat):**\n• Yo como, Tú comes, Él come, Nosotros comemos, Ellos comen\n\n**-IR verbs (vivir - to live):**\n• Yo vivo, Tú vives, Él vive, Nosotros vivimos, Ellos viven",
                "keywords": ["verb", "conjugation", "conjugate", "tense"]
            },
            {
                "question": "How to pronounce Spanish words?",
                "answer": "Spanish pronunciation tips:\n\n**Vowels (always consistent):**\n• A = 'ah' (casa)\n• E = 'eh' (peso)\n• I = 'ee' (sí)\n• O = 'oh' (como)\n• U = 'oo' (tú)\n\n**Special sounds:**\n• ñ = 'ny' (niño)\n• ll = 'y' (pollo)\n• j = hard 'h' (Juan)\n• rr = rolled 'r' (perro)\n• h = silent (hola)\n\nPronunciation is very phonetic - what you see is what you say!",
                "keywords": ["pronunciation", "pronounce", "sound", "speak"]
            },
            {
                "question": "What's the difference between ser and estar?",
                "answer": "Both mean 'to be', but used differently:\n\n**SER (permanent/identity):**\n• Identity: Soy María\n• Origin: Soy de España\n• Characteristics: Es alto (He is tall)\n• Time: Son las dos (It's 2 o'clock)\n• Profession: Soy profesor\n\n**ESTAR (temporary/location):**\n• Location: Estoy en casa\n• Condition: Estoy cansado (I'm tired)\n• Emotions: Está feliz\n• Progressive: Estoy comiendo\n\nSER = What something IS (essence)\nESTAR = How/where something IS (state/location)",
                "keywords": ["ser", "estar", "difference", "be"]
            },
            {
                "question": "Spanish grammar tips",
                "answer": "Essential Spanish grammar tips:\n\n**1. Gender & Articles:**\n• Masculine: el libro (the book) - ends in -o\n• Feminine: la casa (the house) - ends in -a\n• Adjectives must match: el libro rojo, la casa roja\n\n**2. Word Order:**\n• Usually Subject-Verb-Object like English\n• Adjectives often come AFTER nouns\n\n**3. Double Negatives:**\n• No tengo nada (I don't have nothing = I have nothing) ✓\n\n**4. Personal 'a':**\n• Veo a María (I see María) - use 'a' before people\n\n**5. Reflexive Verbs:**\n• Me llamo Juan (My name is Juan)",
                "keywords": ["grammar", "rules", "syntax"]
            },
            {
                "question": "Common Spanish phrases",
                "answer": "Essential Spanish phrases:\n\n**Greetings:**\n• Hola - Hello\n• Buenos días - Good morning\n• Buenas tardes - Good afternoon\n• ¿Cómo estás? - How are you?\n• Bien, gracias - Good, thanks\n\n**Courtesy:**\n• Por favor - Please\n• Gracias - Thank you\n• De nada - You're welcome\n• Perdón - Excuse me/Sorry\n• Lo siento - I'm sorry\n\n**Useful:**\n• No entiendo - I don't understand\n• ¿Hablas inglés? - Do you speak English?\n• ¿Cuánto cuesta? - How much?\n• Me gusta - I like it",
                "keywords": ["phrases", "common", "greetings", "useful"]
            },
            {
                "question": "How to practice Spanish speaking?",
                "answer": "Ways to practice speaking Spanish:\n\n**1. Daily Practice:**\n• Talk to yourself in Spanish\n• Describe what you're doing\n• Think in Spanish when possible\n\n**2. Language Exchange:**\n• Find language partners on Tandem or HelloTalk\n• Join Spanish conversation groups\n\n**3. Shadowing:**\n• Listen to Spanish audio\n• Repeat immediately after\n• Mimic pronunciation\n\n**4. Recording:**\n• Record yourself speaking\n• Compare to native speakers\n\n**Don't fear mistakes** - they're essential for learning!",
                "keywords": ["practice", "speaking", "conversation", "talk"]
            },
            {
                "question": "Spanish vocabulary learning tips",
                "answer": "Effective vocabulary learning strategies:\n\n**1. Thematic Learning:**\nGroup words by theme (food, family, colors)\n\n**2. Use Flashcards:**\n• Physical or digital (Anki, Quizlet)\n• Review with spaced repetition\n\n**3. Context is Key:**\n• Learn phrases, not just words\n• Use words in sentences immediately\n\n**4. Cognates:**\n• Many Spanish-English words are similar\n• hotel = hotel, música = music\n\n**5. Daily Goals:**\n• Learn 5-10 new words daily\n• Review previous words\n• Use them in conversation\n\n**6. Immersion:**\n• Label items at home with Spanish names\n• Change phone language to Spanish",
                "keywords": ["vocabulary", "words", "learn", "memorize"]
            },
            {
                "question": "What are the best Spanish learning resources?",
                "answer": "Recommended Spanish learning resources:\n\n**Apps:**\n• Duolingo - Free, gamified lessons\n• Babbel - Structured courses\n• Memrise - Vocabulary focus\n• Busuu - Community feedback\n\n**Websites:**\n• SpanishDict - Dictionary & grammar\n• StudySpanish.com - Free tutorials\n\n**YouTube Channels:**\n• Butterfly Spanish\n• SpanishPod101\n• Dreaming Spanish\n\n**Podcasts:**\n• Coffee Break Spanish\n• Notes in Spanish\n• Spanish Obsessed\n\n**TV/Movies:**\n• Netflix with Spanish audio/subtitles\n• Money Heist (La Casa de Papel)\n• Elite, Narcos\n\n**Practice:**\n• iTalki - Online tutors\n• Tandem - Language exchange",
                "keywords": ["resources", "apps", "websites", "tools", "recommendations"]
            },
            {
                "question": "How long does it take to learn Spanish?",
                "answer": "Timeline for learning Spanish:\n\n**Basic Conversational (3-6 months):**\n• 15-30 min daily practice\n• Simple conversations\n• Travel basics\n\n**Intermediate (6-12 months):**\n• 30-60 min daily\n• Hold conversations\n• Understand most content\n\n**Advanced/Fluent (1-2 years):**\n• Consistent immersion\n• Complex discussions\n• Read literature\n\n**FSI estimates:** 600-750 class hours for professional proficiency\n\n**Remember:** Everyone learns at their own pace. Consistency matters more than intensity!",
                "keywords": ["how long", "time", "duration", "learn"]
            },
            {
                "question": "Spanish numbers and counting",
                "answer": "Spanish numbers:\n\n**0-10:** cero, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez\n\n**11-20:** once, doce, trece, catorce, quince, dieciséis, diecisiete, dieciocho, diecinueve, veinte\n\n**Tens:** 30-treinta, 40-cuarenta, 50-cincuenta, 60-sesenta, 70-setenta, 80-ochenta, 90-noventa, 100-cien\n\n**Examples:**\n21 - veintiuno\n32 - treinta y dos\n45 - cuarenta y cinco\n\n**Larger:**\n200 - doscientos\n1000 - mil\n1,000,000 - un millón",
                "keywords": ["numbers", "counting", "count"]
            },
            {
                "question": "Spanish days and months",
                "answer": "Days and months in Spanish:\n\n**Days (días):**\n• Lunes - Monday\n• Martes - Tuesday\n• Miércoles - Wednesday\n• Jueves - Thursday\n• Viernes - Friday\n• Sábado - Saturday\n• Domingo - Sunday\n\n**Months (meses):**\n• Enero - January\n• Febrero - February\n• Marzo - March\n• Abril - April\n• Mayo - May\n• Junio - June\n• Julio - July\n• Agosto - August\n• Septiembre - September\n• Octubre - October\n• Noviembre - November\n• Diciembre - December\n\n**Note:** Days and months are NOT capitalized in Spanish!",
                "keywords": ["days", "months", "calendar", "date"]
            },
            {
                "question": "Spanish question words",
                "answer": "Spanish question words (always with accent!):\n\n• ¿Qué? - What?\n• ¿Quién? - Who?\n• ¿Cuándo? - When?\n• ¿Dónde? - Where?\n• ¿Por qué? - Why?\n• ¿Cómo? - How?\n• ¿Cuál? - Which?\n• ¿Cuánto? - How much?\n• ¿Cuántos? - How many?\n\n**Examples:**\n• ¿Qué es esto? - What is this?\n• ¿Dónde está el baño? - Where is the bathroom?\n• ¿Cuánto cuesta? - How much does it cost?\n• ¿Cómo te llamas? - What's your name?\n\n**Remember:** Questions have upside-down ? at start: ¿",
                "keywords": ["question", "questions", "interrogative", "ask"]
            },
            {
                "question": "Spanish food vocabulary",
                "answer": "Common Spanish food vocabulary:\n\n**Meals:**\n• Desayuno - Breakfast\n• Almuerzo - Lunch\n• Cena - Dinner\n\n**Basics:**\n• Pan - Bread\n• Agua - Water\n• Leche - Milk\n• Café - Coffee\n• Arroz - Rice\n• Huevo - Egg\n• Queso - Cheese\n\n**Fruits:**\n• Manzana - Apple\n• Naranja - Orange\n• Plátano - Banana\n• Fresa - Strawberry\n\n**Vegetables:**\n• Tomate - Tomato\n• Lechuga - Lettuce\n• Zanahoria - Carrot\n• Papa/Patata - Potato\n\n**Meat:**\n• Pollo - Chicken\n• Carne - Beef\n• Pescado - Fish\n\n**Phrases:**\n• Tengo hambre - I'm hungry\n• Tengo sed - I'm thirsty\n• ¡Buen provecho! - Enjoy your meal!",
                "keywords": ["food", "vocabulary", "eat", "restaurant"]
            },
            {
                "question": "Spanish alphabet",
                "answer": "The Spanish alphabet has 27 letters (includes Ñ):\n\nA B C D E F G H I J K L M N Ñ O P Q R S T U V W X Y Z\n\n**Important pronunciations:**\n• H is SILENT (hola = OH-la)\n• Ñ makes 'ny' sound (España)\n• J makes hard 'h' sound (José)\n• LL makes 'y' sound (pollo)\n• RR is rolled (perro)\n• V sounds like B (vino)\n• Z is 'th' in Spain, 's' in Latin America\n\n**Vowels are always consistent:**\n• A (ah), E (eh), I (ee), O (oh), U (oo)",
                "keywords": ["alphabet", "letters", "pronunciation"]
            }
        ]
    
    def preprocess_text(self, text):
        """
        Preprocess text for NLP
        - Tokenize
        - Remove stopwords
        - Lemmatize
        """
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and lemmatize
        processed = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalnum() and token not in self.stop_words
        ]
        
        return ' '.join(processed)
    
    def get_response(self, user_message):
        """
        Get chatbot response using NLP similarity matching
        
        Args:
            user_message (str): User's question
        
        Returns:
            str: Bot response
        """
        if not user_message.strip():
            return "Please ask a question about learning Spanish!"
        
        # Vectorize user message
        user_vector = self.vectorizer.transform([user_message])
        
        # Calculate cosine similarity with all questions
        similarities = cosine_similarity(user_vector, self.question_vectors)[0]
        
        # Get best match
        best_match_idx = np.argmax(similarities)
        best_score = similarities[best_match_idx]
        
        # Threshold for similarity (0.15 is fairly lenient)
        if best_score > 0.15:
            return self.answers[best_match_idx]
        else:
            return self._get_default_response()
    
    def _get_default_response(self):
        """Default response when no good match found"""
        return """I'm not sure about that specific question. Here are some topics I can help with:

• Getting started with Spanish
• Grammar and verb conjugations
• Pronunciation tips
• Common phrases and vocabulary
• Learning resources and practice methods
• Days, months, numbers
• Food vocabulary
• Question words

Try asking about one of these topics!"""
    
    def get_all_faqs(self):
        """Return all FAQs for display"""
        return [{'question': q, 'answer': a} for q, a in zip(self.questions, self.answers)]

# Test the chatbot
if __name__ == '__main__':
    print("Testing Spanish Learning Chatbot...")
    bot = SpanishLearningChatbot()
    
    test_questions = [
        "How do I begin learning Spanish?",
        "Tell me about verb conjugations",
        "What's the difference between ser and estar?",
        "How long will it take to learn?",
        "Spanish numbers please"
    ]
    
    print("\n" + "="*60)
    for question in test_questions:
        print(f"\nQ: {question}")
        response = bot.get_response(question)
        print(f"A: {response[:200]}...")
        print("-"*60)
