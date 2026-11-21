"""
Quiz and Assessment System
Multiple types of quizzes for Spanish learning
"""

from backend.models.database import get_db
import random
from datetime import datetime

class QuizSystem:
    """
    Generate and grade quizzes for Spanish learning
    """
    
    def __init__(self):
        self.conn = get_db()
    
    def generate_vocabulary_quiz(self, category=None, count=10):
        """Generate multiple choice vocabulary quiz"""
        cursor = self.conn.cursor()
        
        # Get flashcards
        if category:
            cursor.execute("""
                SELECT * FROM flashcards 
                WHERE category = ?
                ORDER BY RANDOM()
                LIMIT ?
            """, (category, count))
        else:
            cursor.execute("""
                SELECT * FROM flashcards 
                ORDER BY RANDOM()
                LIMIT ?
            """, (count,))
        
        cards = [dict(row) for row in cursor.fetchall()]
        
        quiz_questions = []
        for card in cards:
            # Get wrong answer options
            cursor.execute("""
                SELECT DISTINCT english_word 
                FROM flashcards 
                WHERE id != ? AND category = ?
                ORDER BY RANDOM()
                LIMIT 3
            """, (card['id'], card['category']))
            
            wrong_answers = [row[0] for row in cursor.fetchall()]
            
            # Create options
            options = wrong_answers + [card['english_word']]
            random.shuffle(options)
            
            quiz_questions.append({
                'id': card['id'],
                'question': f"What does '{card['spanish_word']}' mean?",
                'spanish_word': card['spanish_word'],
                'options': options,
                'correct_answer': card['english_word'],
                'example': card.get('example_sentence')
            })
        
        return {
            'quiz_type': 'vocabulary',
            'category': category or 'mixed',
            'questions': quiz_questions
        }
    
    def generate_conjugation_quiz(self, count=10):
        """Generate verb conjugation quiz"""
        verbs = [
            {
                'infinitive': 'hablar',
                'english': 'to speak',
                'type': 'ar',
                'conjugations': {
                    'yo': 'hablo',
                    'tú': 'hablas',
                    'él': 'habla',
                    'nosotros': 'hablamos',
                    'ellos': 'hablan'
                }
            },
            {
                'infinitive': 'comer',
                'english': 'to eat',
                'type': 'er',
                'conjugations': {
                    'yo': 'como',
                    'tú': 'comes',
                    'él': 'come',
                    'nosotros': 'comemos',
                    'ellos': 'comen'
                }
            },
            {
                'infinitive': 'vivir',
                'english': 'to live',
                'type': 'ir',
                'conjugations': {
                    'yo': 'vivo',
                    'tú': 'vives',
                    'él': 'vive',
                    'nosotros': 'vivimos',
                    'ellos': 'viven'
                }
            },
            {
                'infinitive': 'ser',
                'english': 'to be',
                'type': 'irregular',
                'conjugations': {
                    'yo': 'soy',
                    'tú': 'eres',
                    'él': 'es',
                    'nosotros': 'somos',
                    'ellos': 'son'
                }
            },
            {
                'infinitive': 'estar',
                'english': 'to be',
                'type': 'irregular',
                'conjugations': {
                    'yo': 'estoy',
                    'tú': 'estás',
                    'él': 'está',
                    'nosotros': 'estamos',
                    'ellos': 'están'
                }
            },
            {
                'infinitive': 'tener',
                'english': 'to have',
                'type': 'irregular',
                'conjugations': {
                    'yo': 'tengo',
                    'tú': 'tienes',
                    'él': 'tiene',
                    'nosotros': 'tenemos',
                    'ellos': 'tienen'
                }
            }
        ]
        
        quiz_questions = []
        subjects = ['yo', 'tú', 'él', 'nosotros', 'ellos']
        
        for _ in range(min(count, len(verbs) * len(subjects))):
            verb = random.choice(verbs)
            subject = random.choice(subjects)
            
            correct_conjugation = verb['conjugations'][subject]
            
            # Generate wrong options (other conjugations or similar verbs)
            wrong_options = [
                conj for subj, conj in verb['conjugations'].items() 
                if subj != subject
            ][:3]
            
            options = wrong_options + [correct_conjugation]
            random.shuffle(options)
            
            quiz_questions.append({
                'question': f"Conjugate '{verb['infinitive']}' ({verb['english']}) for '{subject}'",
                'infinitive': verb['infinitive'],
                'subject': subject,
                'options': options,
                'correct_answer': correct_conjugation,
                'verb_type': verb['type']
            })
        
        return {
            'quiz_type': 'conjugation',
            'questions': quiz_questions[:count]
        }
    
    def generate_translation_quiz(self, direction='es_to_en', count=10):
        """
        Generate translation quiz
        direction: 'es_to_en' or 'en_to_es'
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM flashcards 
            ORDER BY RANDOM()
            LIMIT ?
        """, (count,))
        
        cards = [dict(row) for row in cursor.fetchall()]
        quiz_questions = []
        
        for card in cards:
            if direction == 'es_to_en':
                question_text = card['spanish_word']
                correct = card['english_word']
                
                # Get wrong options
                cursor.execute("""
                    SELECT english_word FROM flashcards 
                    WHERE id != ?
                    ORDER BY RANDOM()
                    LIMIT 3
                """, (card['id'],))
            else:  # en_to_es
                question_text = card['english_word']
                correct = card['spanish_word']
                
                cursor.execute("""
                    SELECT spanish_word FROM flashcards 
                    WHERE id != ?
                    ORDER BY RANDOM()
                    LIMIT 3
                """, (card['id'],))
            
            wrong_options = [row[0] for row in cursor.fetchall()]
            options = wrong_options + [correct]
            random.shuffle(options)
            
            quiz_questions.append({
                'question': f"Translate: {question_text}",
                'options': options,
                'correct_answer': correct,
                'example': card.get('example_sentence')
            })
        
        return {
            'quiz_type': 'translation',
            'direction': direction,
            'questions': quiz_questions
        }
    
    def generate_grammar_quiz(self, topic='ser_estar', count=10):
        """Generate grammar-focused quiz"""
        grammar_questions = {
            'ser_estar': [
                {
                    'question': 'Yo ___ estudiante. (I am a student)',
                    'options': ['soy', 'estoy', 'es', 'está'],
                    'correct': 'soy',
                    'explanation': 'Use SER for professions/identity'
                },
                {
                    'question': 'Ella ___ cansada. (She is tired)',
                    'options': ['es', 'está', 'son', 'están'],
                    'correct': 'está',
                    'explanation': 'Use ESTAR for temporary conditions'
                },
                {
                    'question': 'Nosotros ___ en casa. (We are at home)',
                    'options': ['somos', 'estamos', 'son', 'están'],
                    'correct': 'estamos',
                    'explanation': 'Use ESTAR for location'
                },
                {
                    'question': 'El libro ___ interesante. (The book is interesting)',
                    'options': ['es', 'está', 'son', 'están'],
                    'correct': 'es',
                    'explanation': 'Use SER for characteristics'
                },
                {
                    'question': '___ las dos. (It is 2 o\'clock)',
                    'options': ['Son', 'Están', 'Es', 'Está'],
                    'correct': 'Son',
                    'explanation': 'Use SER for time'
                }
            ],
            'por_para': [
                {
                    'question': 'Estudio ___ aprender. (I study to learn)',
                    'options': ['para', 'por'],
                    'correct': 'para',
                    'explanation': 'PARA for purpose/goal'
                },
                {
                    'question': 'Gracias ___ tu ayuda. (Thanks for your help)',
                    'options': ['por', 'para'],
                    'correct': 'por',
                    'explanation': 'POR for reason/cause'
                },
                {
                    'question': 'Esto es ___ ti. (This is for you)',
                    'options': ['para', 'por'],
                    'correct': 'para',
                    'explanation': 'PARA for recipient'
                },
                {
                    'question': 'Caminamos ___ el parque. (We walk through the park)',
                    'options': ['por', 'para'],
                    'correct': 'por',
                    'explanation': 'POR for through/movement'
                }
            ]
        }
        
        questions = grammar_questions.get(topic, grammar_questions['ser_estar'])
        selected = random.sample(questions, min(count, len(questions)))
        
        return {
            'quiz_type': 'grammar',
            'topic': topic,
            'questions': selected
        }
    
    def grade_quiz(self, user_id, quiz_type, topic, answers, questions):
        """
        Grade quiz and save results
        
        Args:
            user_id: User ID
            quiz_type: Type of quiz
            topic: Quiz topic/category
            answers: List of user answers
            questions: Original questions with correct answers
        
        Returns:
            Results dictionary with score and feedback
        """
        correct_count = 0
        results = []
        
        for i, (answer, question) in enumerate(zip(answers, questions)):
            correct = answer == question['correct_answer']
            if correct:
                correct_count += 1
            
            results.append({
                'question_num': i + 1,
                'question': question['question'],
                'user_answer': answer,
                'correct_answer': question['correct_answer'],
                'is_correct': correct,
                'explanation': question.get('explanation')
            })
        
        total_questions = len(questions)
        score = int((correct_count / total_questions) * 100)
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_results 
            (user_id, quiz_type, topic, score, total_questions)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, quiz_type, topic, score, total_questions))
        self.conn.commit()
        
        # Determine feedback
        if score >= 90:
            feedback = "¡Excelente! Excellent work! 🌟"
        elif score >= 75:
            feedback = "¡Muy bien! Very good! Keep it up! 👍"
        elif score >= 60:
            feedback = "¡Bien! Good effort! Keep practicing! 📚"
        else:
            feedback = "Keep studying! You're making progress! 💪"
        
        return {
            'score': score,
            'correct': correct_count,
            'total': total_questions,
            'percentage': score,
            'feedback': feedback,
            'results': results
        }
    
    def get_user_quiz_history(self, user_id, limit=10):
        """Get user's quiz history"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT quiz_type, topic, score, total_questions, created_at
            FROM quiz_results
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_quiz_stats(self, user_id):
        """Get overall quiz statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_quizzes,
                AVG(score) as avg_score,
                MAX(score) as best_score,
                SUM(total_questions) as total_questions_answered
            FROM quiz_results
            WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        
        return {
            'total_quizzes': row[0] or 0,
            'average_score': round(row[1] or 0, 1),
            'best_score': row[2] or 0,
            'total_questions': row[3] or 0
        }


# Test
if __name__ == '__main__':
    print("Testing Quiz System...")
    from database import init_db, seed_flashcards
    
    init_db()
    seed_flashcards()
    
    qs = QuizSystem()
    
    # Test vocabulary quiz
    vocab_quiz = qs.generate_vocabulary_quiz('greetings', count=3)
    print(f"\nVocabulary Quiz ({vocab_quiz['category']}):")
    for i, q in enumerate(vocab_quiz['questions'], 1):
        print(f"{i}. {q['question']}")
        print(f"   Options: {q['options']}")
        print(f"   Answer: {q['correct_answer']}")
    
    # Test conjugation quiz
    conj_quiz = qs.generate_conjugation_quiz(count=3)
    print(f"\nConjugation Quiz:")
    for i, q in enumerate(conj_quiz['questions'], 1):
        print(f"{i}. {q['question']}")
        print(f"   Answer: {q['correct_answer']}")
    
    # Test grammar quiz
    grammar_quiz = qs.generate_grammar_quiz('ser_estar', count=3)
    print(f"\nGrammar Quiz (ser/estar):")
    for i, q in enumerate(grammar_quiz['questions'], 1):
        print(f"{i}. {q['question']}")
        print(f"   Answer: {q['correct']}")
    
    # Test grading
    test_answers = [q['correct_answer'] for q in vocab_quiz['questions']]
    results = qs.grade_quiz(1, 'vocabulary', 'greetings', test_answers, vocab_quiz['questions'])
    print(f"\nGrading Results:")
    print(f"Score: {results['score']}%")
    print(f"Feedback: {results['feedback']}")
