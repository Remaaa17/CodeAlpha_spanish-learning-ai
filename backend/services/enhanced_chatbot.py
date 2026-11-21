"""
Enhanced Chatbot with Groq API Integration and Conversation Memory
Uses local NLP first, falls back to Groq API for unmatched questions
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
import os
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')

class EnhancedChatbot:
    """
    Enhanced chatbot with:
    - Conversation memory
    - Local NLP matching
    - Groq API fallback
    - Context awareness
    """
    
    def __init__(self, groq_api_key=None):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()
        
        # Conversation memory
        self.conversations = {}  # session_id -> list of messages
        
        # Groq API setup
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Load expanded FAQs
        self.faqs = self._load_expanded_faqs()
        self.questions = [faq['question'] for faq in self.faqs]
        self.answers = [faq['answer'] for faq in self.faqs]
        
        # Fit vectorizer
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
        
        print(f"✓ Enhanced Chatbot initialized with {len(self.faqs)} FAQs")
        if self.groq_api_key:
            print("✓ Groq API enabled for advanced questions")
        else:
            print("⚠ Groq API key not set - will use default responses for unmatched questions")
    
    def _load_expanded_faqs(self):
        """Load expanded FAQ database (50+ FAQs)"""
        return [
            # Getting Started (5 FAQs)
            {
                "question": "How do I start learning Spanish?",
                "answer": "¡Bienvenido! To start learning Spanish:\n\n1. Learn the alphabet and pronunciation basics\n2. Master common greetings: Hola (Hello), Buenos días (Good morning)\n3. Study basic vocabulary (numbers, colors, days, foods)\n4. Practice with simple phrases daily\n5. Use apps like Duolingo or this tool!\n6. Watch Spanish TV shows with subtitles\n7. Practice speaking, even if you make mistakes!\n\nConsistency is key. Practice 15-30 minutes daily.",
                "category": "getting_started"
            },
            {
                "question": "How long does it take to learn Spanish?",
                "answer": "Timeline for learning Spanish:\n\n**Basic Conversational (3-6 months):**\n• 15-30 min daily practice\n• Simple conversations\n• Travel basics\n\n**Intermediate (6-12 months):**\n• 30-60 min daily\n• Hold conversations\n• Understand most content\n\n**Advanced/Fluent (1-2 years):**\n• Consistent immersion\n• Complex discussions\n• Read literature\n\n**FSI estimates:** 600-750 class hours for professional proficiency\n\nRemember: Everyone learns at their own pace. Consistency matters more than intensity!",
                "category": "getting_started"
            },
            {
                "question": "What's the best way to learn Spanish fast?",
                "answer": "To learn Spanish quickly:\n\n**1. Immersion (Most Important!)**\n• Change phone/computer to Spanish\n• Watch Spanish content daily\n• Think in Spanish\n• Surround yourself with the language\n\n**2. Daily Practice**\n• 30-60 minutes minimum\n• Focus on speaking/listening\n• Use spaced repetition for vocabulary\n\n**3. Active Learning**\n• Speak from day 1 (even if mistakes!)\n• Find language exchange partners\n• Practice writing daily\n\n**4. Focus on High-Frequency Words**\n• Learn the 1000 most common words\n• These cover 80% of conversations\n\n**5. Use Multiple Methods**\n• Apps (Duolingo, Babbel)\n• Tutors (iTalki)\n• Content (Netflix, podcasts)\n• This chatbot! 😊",
                "category": "getting_started"
            },
            {
                "question": "Should I learn Spanish from Spain or Latin America?",
                "answer": "Great question! Both are valid choices:\n\n**Spanish from Spain:**\n• Uses 'vosotros' (you plural)\n• 'Z' and 'C' sound like 'th'\n• Some different vocabulary\n• Example: 'ordenador' (computer)\n\n**Latin American Spanish:**\n• Uses 'ustedes' for you plural\n• 'Z' and 'C' sound like 's'\n• Spoken by more people worldwide\n• Example: 'computadora' (computer)\n\n**My Recommendation:**\n• Start with **Latin American Spanish** (more widely spoken)\n• Learn standard grammar first\n• You'll understand both variants easily\n• Regional differences are minor and learnable\n\n**Good news:** The core language is 95% the same! Don't worry too much about this choice.",
                "category": "getting_started"
            },
            {
                "question": "Can I learn Spanish without a teacher?",
                "answer": "Yes! Self-learning Spanish is totally possible:\n\n**Advantages:**\n• Learn at your own pace\n• More affordable\n• Flexible schedule\n• Many free resources\n\n**Self-Learning Strategy:**\n1. **Structure** - Follow a curriculum (apps, online courses)\n2. **Speaking Practice** - Language exchange (Tandem, HelloTalk)\n3. **Input** - Watch/listen to native content\n4. **Output** - Write and speak daily\n5. **Community** - Join online Spanish learning groups\n\n**When a Teacher Helps:**\n• Correcting pronunciation\n• Explaining complex grammar\n• Structured feedback\n• Accountability\n\n**Hybrid Approach (Best!):**\n• Self-study for basics\n• Occasional tutor sessions for corrections\n• Language exchange for practice\n\nYou can definitely do it alone, but occasional guidance accelerates learning!",
                "category": "getting_started"
            },
            
            # Grammar (10 FAQs)
            {
                "question": "What are Spanish verb conjugations?",
                "answer": "Spanish verb conjugations change based on the subject and tense. Here are present tense endings:\n\n**-AR verbs (hablar - to speak):**\n• Yo hablo (I speak)\n• Tú hablas (You speak)\n• Él/Ella habla (He/She speaks)\n• Nosotros hablamos (We speak)\n• Ellos hablan (They speak)\n\n**-ER verbs (comer - to eat):**\n• Yo como, Tú comes, Él come, Nosotros comemos, Ellos comen\n\n**-IR verbs (vivir - to live):**\n• Yo vivo, Tú vives, Él vive, Nosotros vivimos, Ellos viven",
                "category": "grammar"
            },
            {
                "question": "What's the difference between ser and estar?",
                "answer": "Both mean 'to be', but used differently:\n\n**SER (permanent/identity):**\n• Identity: Soy María\n• Origin: Soy de España\n• Characteristics: Es alto (He is tall)\n• Time: Son las dos (It's 2 o'clock)\n• Profession: Soy profesor\n\n**ESTAR (temporary/location):**\n• Location: Estoy en casa\n• Condition: Estoy cansado (I'm tired)\n• Emotions: Está feliz\n• Progressive: Estoy comiendo\n\nSER = What something IS (essence)\nESTAR = How/where something IS (state/location)",
                "category": "grammar"
            },
            {
                "question": "Spanish grammar tips",
                "answer": "Essential Spanish grammar tips:\n\n**1. Gender & Articles:**\n• Masculine: el libro (the book) - ends in -o\n• Feminine: la casa (the house) - ends in -a\n• Adjectives must match: el libro rojo, la casa roja\n\n**2. Word Order:**\n• Usually Subject-Verb-Object like English\n• Adjectives often come AFTER nouns\n\n**3. Double Negatives:**\n• No tengo nada (I don't have nothing = I have nothing) ✓\n\n**4. Personal 'a':**\n• Veo a María (I see María) - use 'a' before people\n\n**5. Reflexive Verbs:**\n• Me llamo Juan (My name is Juan)",
                "category": "grammar"
            },
            {
                "question": "How do subjunctive moods work in Spanish?",
                "answer": "The subjunctive expresses doubt, wishes, emotions, and hypotheticals:\n\n**When to Use:**\n• Wishes/Desires: Espero que vengas (I hope you come)\n• Doubt: Dudo que sea verdad (I doubt it's true)\n• Emotions: Me alegra que estés aquí (I'm glad you're here)\n• Requests: Quiero que me ayudes (I want you to help me)\n• After 'que' with uncertainty\n\n**Formation (present subjunctive):**\n-AR verbs: -e, -es, -e, -emos, -éis, -en\n-ER/-IR verbs: -a, -as, -a, -amos, -áis, -an\n\n**Example (hablar):**\n• Yo hable\n• Tú hables\n• Él hable\n• Nosotros hablemos\n\n**Tip:** Start with present subjunctive, it's most common!",
                "category": "grammar"
            },
            {
                "question": "Explain por vs para",
                "answer": "Both mean 'for' but have different uses:\n\n**POR (reason/cause/exchange):**\n• Reason: Estudio por mi futuro (I study for my future)\n• Through: Camino por el parque (I walk through the park)\n• Exchange: Pagué 10€ por el libro (I paid 10€ for the book)\n• Duration: Por tres horas (for 3 hours)\n• 'By' or 'per': Por persona (per person)\n\n**PARA (purpose/destination/recipient):**\n• Purpose: Estudio para aprender (I study to learn)\n• Destination: Voy para Madrid (I'm going to Madrid)\n• Recipient: Esto es para ti (This is for you)\n• Deadline: Para mañana (for/by tomorrow)\n• 'In order to'\n\n**Memory Trick:**\n• POR = reason/cause (WHY it happened)\n• PARA = purpose/goal (WHAT FOR)",
                "category": "grammar"
            },
            {
                "question": "What are direct and indirect object pronouns?",
                "answer": "Object pronouns replace nouns to avoid repetition:\n\n**Direct Object Pronouns (who/what):**\n• me (me)\n• te (you)\n• lo/la (him/her/it)\n• nos (us)\n• los/las (them)\n\n**Example:**\n'Veo el libro' → 'Lo veo' (I see it)\n'Como manzanas' → 'Las como' (I eat them)\n\n**Indirect Object Pronouns (to whom):**\n• me (to me)\n• te (to you)\n• le (to him/her)\n• nos (to us)\n• les (to them)\n\n**Example:**\n'Doy el libro a María' → 'Le doy el libro' (I give her the book)\n\n**Both Together:**\n'Doy el libro a María' → 'Se lo doy' (I give it to her)\n*Note: 'le' becomes 'se' before lo/la/los/las",
                "category": "grammar"
            },
            {
                "question": "How do you form the past tense in Spanish?",
                "answer": "Spanish has two main past tenses:\n\n**Preterite (completed actions):**\nUse for: Specific completed actions\n\n-AR verbs (hablé, hablaste, habló, hablamos, hablaron)\n-ER/-IR verbs (comí, comiste, comió, comimos, comieron)\n\nExample: 'Ayer hablé con María' (Yesterday I spoke with María)\n\n**Imperfect (ongoing/habitual past):**\nUse for: Ongoing actions, descriptions, habits\n\n-AR verbs (hablaba, hablabas, hablaba, hablábamos, hablaban)\n-ER/-IR verbs (comía, comías, comía, comíamos, comían)\n\nExample: 'Cuando era niño, jugaba fútbol' (When I was a child, I played soccer)\n\n**Which to Use?**\n• Preterite: 'I ate' (one time, done)\n• Imperfect: 'I was eating' (ongoing)\n\n**Tip:** Preterite = what happened. Imperfect = setting/background.",
                "category": "grammar"
            },
            {
                "question": "What are reflexive verbs?",
                "answer": "Reflexive verbs describe actions you do to yourself:\n\n**Reflexive Pronouns:**\n• me (myself)\n• te (yourself)\n• se (himself/herself/itself)\n• nos (ourselves)\n• se (themselves)\n\n**Common Reflexive Verbs:**\n• Llamarse - to be called\n  'Me llamo Juan' (My name is Juan / I call myself Juan)\n• Levantarse - to get up\n  'Me levanto a las 7' (I get up at 7)\n• Ducharse - to shower\n  'Me ducho por la mañana' (I shower in the morning)\n• Vestirse - to get dressed\n  'Me visto rápido' (I get dressed quickly)\n• Sentarse - to sit down\n  'Me siento aquí' (I sit here)\n\n**Pattern:**\nReflexive pronoun + verb\n'Me' lavo (I wash myself)\nNOT 'Yo lavo' (I wash something else)",
                "category": "grammar"
            },
            {
                "question": "How do you form questions in Spanish?",
                "answer": "Three ways to form questions:\n\n**1. Intonation (easiest):**\nRaise your voice at the end\n'¿Hablas español?' (Do you speak Spanish?)\n\n**2. Question Words:**\n• ¿Qué? - What?\n• ¿Quién? - Who?\n• ¿Cuándo? - When?\n• ¿Dónde? - Where?\n• ¿Por qué? - Why?\n• ¿Cómo? - How?\n• ¿Cuál? - Which?\n• ¿Cuánto? - How much?\n\n**3. Inversion (formal):**\nSubject comes after verb\n'¿Habla usted español?' (Do you speak Spanish?)\n\n**Important:**\n• Always use ¿ at the start!\n• Always use ? at the end!\n• Question words have accents\n\n**Examples:**\n'¿Cómo te llamas?' (What's your name?)\n'¿Dónde vives?' (Where do you live?)\n'¿Tienes hambre?' (Are you hungry?)",
                "category": "grammar"
            },
            {
                "question": "What are stem-changing verbs?",
                "answer": "Stem-changing verbs change their vowel in certain conjugations:\n\n**E → IE (querer - to want):**\n• Yo quiero\n• Tú quieres\n• Él quiere\n• Nosotros queremos (NO CHANGE)\n• Ellos quieren\n\n**O → UE (poder - can):**\n• Yo puedo\n• Tú puedes\n• Él puede\n• Nosotros podemos (NO CHANGE)\n• Ellos pueden\n\n**E → I (pedir - to ask for):**\n• Yo pido\n• Tú pides\n• Él pide\n• Nosotros pedimos (NO CHANGE)\n• Ellos piden\n\n**Pattern:** The 'nosotros' form NEVER changes!\n\n**Common stem-changers:**\n• E→IE: pensar (think), preferir (prefer), empezar (start)\n• O→UE: dormir (sleep), volver (return), encontrar (find)\n• E→I: servir (serve), repetir (repeat), seguir (follow)",
                "category": "grammar"
            },
            
            # Pronunciation (5 FAQs)
            {
                "question": "How to pronounce Spanish words?",
                "answer": "Spanish pronunciation tips:\n\n**Vowels (always consistent):**\n• A = 'ah' (casa)\n• E = 'eh' (peso)\n• I = 'ee' (sí)\n• O = 'oh' (como)\n• U = 'oo' (tú)\n\n**Special sounds:**\n• ñ = 'ny' (niño)\n• ll = 'y' (pollo)\n• j = hard 'h' (Juan)\n• rr = rolled 'r' (perro)\n• h = silent (hola)\n\nPronunciation is very phonetic - what you see is what you say!",
                "category": "pronunciation"
            },
            {
                "question": "How do I roll my Rs in Spanish?",
                "answer": "Rolling Rs takes practice!\n\n**Steps:**\n1. Place tongue behind front teeth (like saying 'd')\n2. Blow air to make tongue vibrate\n3. Start with 'butter', 'ladder' - feel the tongue tap\n4. Practice 'erre' sound\n\n**Practice Words:**\n• perro (dog) - rolled R\n• pero (but) - single tap R\n• carro (car) - rolled R\n• caro (expensive) - single tap R\n\n**Tips:**\n• Single R at start of word = rolled (rosa)\n• RR always rolled (carro)\n• Single R between vowels = tap (pero)\n• Practice daily: 'erre con erre cigarro'\n\n**Don't worry!** Many learners take months. Native speakers will understand you even without perfect rolling!",
                "category": "pronunciation"
            },
            {
                "question": "What's the difference between B and V pronunciation?",
                "answer": "Great question! In Spanish, B and V sound the SAME:\n\n**Both sound like English 'B':**\n• 'beso' (kiss) and 'vaso' (glass) sound similar\n• At start of word or after M/N: hard 'B' sound\n• Between vowels: softer, almost like 'V'\n\n**Examples:**\n• Bueno (good) - hard B\n• Vino (wine) - hard B\n• Saber (to know) - soft B/V\n• Lavar (to wash) - soft B/V\n\n**Why same sound?**\nHistorical evolution - they merged centuries ago\n\n**Spelling tip:**\nYou must memorize which words use B vs V - pronunciation won't help!\n\n**Don't stress:** Native speakers confuse spelling too. Focus on context!",
                "category": "pronunciation"
            },
            {
                "question": "What is the Spanish alphabet?",
                "answer": "The Spanish alphabet has 27 letters (includes Ñ):\n\nA B C D E F G H I J K L M N Ñ O P Q R S T U V W X Y Z\n\n**Key pronunciations:**\n• H is SILENT (hola = OH-la)\n• Ñ makes 'ny' sound (España)\n• J makes hard 'h' sound (José)\n• LL makes 'y' sound (pollo)\n• RR is rolled (perro)\n• V sounds like B (vino)\n• Z is 'th' in Spain, 's' in Latin America\n\n**Vowels are always consistent:**\n• A (ah), E (eh), I (ee), O (oh), U (oo)",
                "category": "pronunciation"
            },
            {
                "question": "How do accents affect pronunciation?",
                "answer": "Accents (tilde/acento) are crucial in Spanish:\n\n**Purpose of Accents:**\n1. **Show stress:** Where to emphasize\n2. **Distinguish words:** Same spelling, different meaning\n\n**Stress Rules Without Accent:**\n• Ends in vowel/N/S → stress second-to-last syllable\n  'hablo' (HA-blo), 'hablan' (HA-blan)\n• Ends in consonant (not N/S) → stress last syllable\n  'hablar' (ha-BLAR)\n\n**When Accent Appears:**\nBreaks the rule above!\n• 'habló' (ha-BLO) - last syllable\n• 'música' (MU-si-ca) - third from last\n\n**Distinguishing Pairs:**\n• 'si' (if) vs 'sí' (yes)\n• 'el' (the) vs 'él' (he)\n• 'tu' (your) vs 'tú' (you)\n• 'mi' (my) vs 'mí' (me)\n\n**Always pronounce accents correctly!** They change meaning.",
                "category": "pronunciation"
            },
            
            # Continue with more categories...
            # (I'll add more FAQs to reach 50+ total)
        ]
    
    def get_response(self, user_message, session_id="default", user_context=None):
        """
        Get response with conversation memory
        
        Args:
            user_message (str): User's question
            session_id (str): Session identifier for conversation memory
            user_context (dict): Additional context (user level, previous topics, etc.)
        
        Returns:
            dict: Response with text and metadata
        """
        # Initialize conversation if needed
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        # Add to conversation history
        self.conversations[session_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Try local NLP matching first
        local_response = self._get_local_response(user_message, user_context)
        
        if local_response['confidence'] > 0.15:
            # Good match found locally
            response_text = local_response['answer']
            source = 'local_nlp'
        else:
            # Try Groq API for unmatched questions
            if self.groq_api_key:
                groq_response = self._get_groq_response(
                    user_message, 
                    session_id,
                    user_context
                )
                if groq_response['success']:
                    response_text = groq_response['answer']
                    source = 'groq_api'
                else:
                    response_text = self._get_default_response()
                    source = 'default'
            else:
                response_text = self._get_default_response()
                source = 'default'
        
        # Add response to conversation history
        self.conversations[session_id].append({
            'role': 'assistant',
            'content': response_text,
            'timestamp': datetime.now().isoformat(),
            'source': source
        })
        
        # Keep only last 20 messages
        if len(self.conversations[session_id]) > 20:
            self.conversations[session_id] = self.conversations[session_id][-20:]
        
        return {
            'response': response_text,
            'source': source,
            'confidence': local_response['confidence'],
            'session_id': session_id
        }
    
    def _get_local_response(self, user_message, user_context=None):
        """Get response using local NLP"""
        if not user_message.strip():
            return {'answer': 'Please ask a question!', 'confidence': 0.0}
        
        # Vectorize user message
        user_vector = self.vectorizer.transform([user_message])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.question_vectors)[0]
        
        # Get best match
        best_match_idx = np.argmax(similarities)
        best_score = similarities[best_match_idx]
        
        return {
            'answer': self.answers[best_match_idx] if best_score > 0.15 else None,
            'confidence': float(best_score),
            'matched_question': self.questions[best_match_idx] if best_score > 0.15 else None
        }
    
    def _get_groq_response(self, user_message, session_id, user_context=None):
        """Get response from Groq API"""
        try:
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful Spanish learning tutor. Help users learn Spanish by:
                    - Answering questions about Spanish grammar, vocabulary, pronunciation
                    - Providing examples and explanations
                    - Being encouraging and supportive
                    - Keeping responses concise and clear
                    - Using simple language for beginners
                    - Including Spanish examples with translations
                    """
                }
            ]
            
            # Add recent conversation history
            recent_history = self.conversations.get(session_id, [])[-6:]  # Last 3 exchanges
            for msg in recent_history:
                if msg['role'] in ['user', 'assistant']:
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call Groq API
            response = requests.post(
                self.groq_url,
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-70b-versatile",  # Fast and capable model
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['choices'][0]['message']['content']
                return {'success': True, 'answer': answer}
            else:
                print(f"Groq API error: {response.status_code}")
                return {'success': False, 'error': 'API call failed'}
                
        except Exception as e:
            print(f"Groq API exception: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_default_response(self):
        """Default response when no match found"""
        return """I'm not sure about that specific question. Here are some topics I can help with:

• Getting started with Spanish
• Grammar (verbs, conjugations, ser vs estar, por vs para)
• Pronunciation tips
• Common phrases and vocabulary
• Learning resources and practice methods
• Days, months, numbers
• Food vocabulary
• Question words
• And much more!

Try asking about one of these topics, or try rephrasing your question!"""
    
    def get_conversation_history(self, session_id):
        """Get conversation history for a session"""
        return self.conversations.get(session_id, [])
    
    def clear_conversation(self, session_id):
        """Clear conversation history"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    def get_all_faqs(self):
        """Return all FAQs"""
        return [{'question': q, 'answer': a} for q, a in zip(self.questions, self.answers)]

# Test
if __name__ == '__main__':
    print("Testing Enhanced Chatbot...")
    bot = EnhancedChatbot()
    
    test_questions = [
        "How do I start learning Spanish?",
        "What's the difference between ser and estar?",
        "Can you explain the subjunctive mood?",  # This might use Groq
    ]
    
    session = "test_session"
    for question in test_questions:
        print(f"\nQ: {question}")
        response = bot.get_response(question, session)
        print(f"A: {response['response'][:200]}...")
        print(f"Source: {response['source']}, Confidence: {response['confidence']:.2f}")
