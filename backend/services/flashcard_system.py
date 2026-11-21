"""
Flashcard System with Spaced Repetition
"""

from backend.models.database import get_db
from datetime import datetime, timedelta
import random

class FlashcardSystem:
    """
    Flashcard system with spaced repetition algorithm
    """
    
    def __init__(self):
        self.conn = get_db()
    
    def get_flashcards_by_category(self, category=None, difficulty=None, limit=20):
        """Get flashcards filtered by category and difficulty"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM flashcards WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)
        
        query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_categories(self):
        """Get all flashcard categories"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM flashcards")
        return [row[0] for row in cursor.fetchall()]
    
    def get_due_cards(self, user_id, limit=10):
        """
        Get cards due for review using spaced repetition
        """
        cursor = self.conn.cursor()
        
        # Cards that haven't been reviewed yet OR are due for review
        query = """
            SELECT f.*, 
                   COALESCE(fp.correct_count, 0) as correct_count,
                   COALESCE(fp.incorrect_count, 0) as incorrect_count,
                   fp.next_review
            FROM flashcards f
            LEFT JOIN flashcard_progress fp ON f.id = fp.flashcard_id AND fp.user_id = ?
            WHERE fp.next_review IS NULL OR fp.next_review <= DATE('now')
            ORDER BY RANDOM()
            LIMIT ?
        """
        
        cursor.execute(query, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    def record_review(self, user_id, flashcard_id, correct):
        """
        Record flashcard review and calculate next review date
        Uses spaced repetition algorithm
        """
        cursor = self.conn.cursor()
        
        # Get current progress
        cursor.execute("""
            SELECT correct_count, incorrect_count 
            FROM flashcard_progress 
            WHERE user_id = ? AND flashcard_id = ?
        """, (user_id, flashcard_id))
        
        row = cursor.fetchone()
        
        if row:
            correct_count = row[0] + (1 if correct else 0)
            incorrect_count = row[1] + (0 if correct else 1)
        else:
            correct_count = 1 if correct else 0
            incorrect_count = 0 if correct else 1
        
        # Calculate next review date using spaced repetition
        if correct:
            # Increase interval based on correct streak
            if correct_count == 1:
                days_until_review = 1  # Review tomorrow
            elif correct_count == 2:
                days_until_review = 3  # 3 days
            elif correct_count == 3:
                days_until_review = 7  # 1 week
            elif correct_count >= 4:
                days_until_review = 14  # 2 weeks
            else:
                days_until_review = 30  # 1 month
        else:
            # Reset to short interval if incorrect
            days_until_review = 1
            correct_count = 0  # Reset streak
        
        next_review = (datetime.now() + timedelta(days=days_until_review)).date()
        
        # Update or insert progress
        cursor.execute("""
            INSERT INTO flashcard_progress 
            (user_id, flashcard_id, correct_count, incorrect_count, last_reviewed, next_review)
            VALUES (?, ?, ?, ?, DATE('now'), ?)
            ON CONFLICT(user_id, flashcard_id) 
            DO UPDATE SET
                correct_count = ?,
                incorrect_count = ?,
                last_reviewed = DATE('now'),
                next_review = ?
        """, (user_id, flashcard_id, correct_count, incorrect_count, next_review,
              correct_count, incorrect_count, next_review))
        
        self.conn.commit()
        
        return {
            'next_review': next_review.isoformat(),
            'correct_count': correct_count,
            'incorrect_count': incorrect_count
        }
    
    def get_user_stats(self, user_id):
        """Get user's flashcard statistics"""
        cursor = self.conn.cursor()
        
        # Total cards
        cursor.execute("SELECT COUNT(*) FROM flashcards")
        total_cards = cursor.fetchone()[0]
        
        # Cards studied
        cursor.execute("""
            SELECT COUNT(DISTINCT flashcard_id) 
            FROM flashcard_progress 
            WHERE user_id = ?
        """, (user_id,))
        cards_studied = cursor.fetchone()[0]
        
        # Mastered cards (3+ correct in a row)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM flashcard_progress 
            WHERE user_id = ? AND correct_count >= 3
        """, (user_id,))
        mastered_cards = cursor.fetchone()[0]
        
        # Cards due today
        cursor.execute("""
            SELECT COUNT(*) 
            FROM flashcard_progress 
            WHERE user_id = ? AND next_review <= DATE('now')
        """, (user_id,))
        due_today = cursor.fetchone()[0]
        
        # Accuracy rate
        cursor.execute("""
            SELECT 
                SUM(correct_count) as total_correct,
                SUM(correct_count + incorrect_count) as total_reviews
            FROM flashcard_progress 
            WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        
        if row[1] and row[1] > 0:
            accuracy = (row[0] / row[1]) * 100
        else:
            accuracy = 0
        
        return {
            'total_cards': total_cards,
            'cards_studied': cards_studied,
            'mastered_cards': mastered_cards,
            'due_today': due_today,
            'accuracy': round(accuracy, 1)
        }
    
    def create_custom_card(self, spanish_word, english_word, category, 
                          difficulty='easy', example_sentence=None):
        """Create a custom flashcard"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO flashcards 
            (spanish_word, english_word, category, difficulty, example_sentence)
            VALUES (?, ?, ?, ?, ?)
        """, (spanish_word, english_word, category, difficulty, example_sentence))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_practice_session(self, user_id, count=10, category=None):
        """
        Get a practice session of flashcards
        Mix of: due cards, new cards, and random review
        """
        # Get due cards (priority)
        due_cards = self.get_due_cards(user_id, limit=count // 2)
        
        # Get new cards (never seen)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT f.* 
            FROM flashcards f
            LEFT JOIN flashcard_progress fp ON f.id = fp.flashcard_id AND fp.user_id = ?
            WHERE fp.flashcard_id IS NULL
            ORDER BY RANDOM()
            LIMIT ?
        """, (user_id, count - len(due_cards)))
        
        new_cards = [dict(row) for row in cursor.fetchall()]
        
        # Combine and shuffle
        session_cards = due_cards + new_cards
        random.shuffle(session_cards)
        
        return session_cards[:count]


# Test
if __name__ == '__main__':
    print("Testing Flashcard System...")
    from database import init_db, seed_flashcards
    
    # Initialize
    init_db()
    seed_flashcards()
    
    fs = FlashcardSystem()
    
    # Test categories
    print("\nCategories:", fs.get_categories())
    
    # Test getting cards
    cards = fs.get_flashcards_by_category('greetings', limit=5)
    print(f"\nGreeting cards: {len(cards)}")
    for card in cards:
        print(f"  {card['spanish_word']} = {card['english_word']}")
    
    # Test practice session
    test_user_id = 1
    session = fs.get_practice_session(test_user_id, count=5)
    print(f"\nPractice session: {len(session)} cards")
    
    # Test recording review
    if session:
        result = fs.record_review(test_user_id, session[0]['id'], correct=True)
        print(f"\nRecorded review: {result}")
    
    # Test stats
    stats = fs.get_user_stats(test_user_id)
    print(f"\nUser stats: {stats}")
