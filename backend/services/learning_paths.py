"""
Learning Paths and Progress Tracking
Structured curriculum for Spanish learning
"""

from backend.models.database import get_db
from datetime import datetime

class LearningPaths:
    """
    Manage learning paths and track user progress
    """
    
    def __init__(self):
        self.conn = get_db()
        self.paths = self._define_paths()
    
    def _define_paths(self):
        """Define learning paths for different levels"""
        return {
            'beginner': {
                'name': 'Beginner Path',
                'description': 'Start your Spanish journey',
                'estimated_weeks': 8,
                'lessons': [
                    {
                        'id': 'beg_1',
                        'title': 'Spanish Alphabet & Pronunciation',
                        'description': 'Learn the Spanish alphabet and basic pronunciation rules',
                        'topics': ['alphabet', 'vowels', 'consonants', 'accents'],
                        'activities': ['pronunciation_practice', 'listening'],
                        'estimated_hours': 2
                    },
                    {
                        'id': 'beg_2',
                        'title': 'Greetings & Introductions',
                        'description': 'Common greetings and how to introduce yourself',
                        'topics': ['hola', 'buenos días', 'me llamo', 'mucho gusto'],
                        'activities': ['flashcards', 'conversation'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'beg_3',
                        'title': 'Numbers 1-100',
                        'description': 'Count and use numbers in Spanish',
                        'topics': ['1-10', '11-20', '21-100'],
                        'activities': ['counting_practice', 'quiz'],
                        'estimated_hours': 2
                    },
                    {
                        'id': 'beg_4',
                        'title': 'Common Phrases',
                        'description': 'Essential phrases for daily use',
                        'topics': ['por favor', 'gracias', 'perdón', 'no entiendo'],
                        'activities': ['flashcards', 'conversation'],
                        'estimated_hours': 2
                    },
                    {
                        'id': 'beg_5',
                        'title': 'Colors & Objects',
                        'description': 'Learn colors and common objects',
                        'topics': ['colors', 'classroom objects', 'household items'],
                        'activities': ['flashcards', 'quiz'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'beg_6',
                        'title': 'Days, Months & Time',
                        'description': 'Talk about time, days, and months',
                        'topics': ['days of week', 'months', 'telling time'],
                        'activities': ['flashcards', 'conversation'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'beg_7',
                        'title': 'Present Tense -AR Verbs',
                        'description': 'Your first verb conjugations',
                        'topics': ['hablar', 'estudiar', 'trabajar'],
                        'activities': ['conjugation_practice', 'quiz'],
                        'estimated_hours': 4
                    },
                    {
                        'id': 'beg_8',
                        'title': 'Family & Relationships',
                        'description': 'Talk about family members',
                        'topics': ['madre', 'padre', 'hermano', 'family vocabulary'],
                        'activities': ['flashcards', 'conversation'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'beg_9',
                        'title': 'Food & Restaurants',
                        'description': 'Order food and discuss meals',
                        'topics': ['food vocabulary', 'restaurant phrases', 'preferences'],
                        'activities': ['flashcards', 'role-play'],
                        'estimated_hours': 4
                    },
                    {
                        'id': 'beg_10',
                        'title': 'Present Tense -ER/-IR Verbs',
                        'description': 'Complete present tense conjugations',
                        'topics': ['comer', 'vivir', 'escribir'],
                        'activities': ['conjugation_practice', 'quiz'],
                        'estimated_hours': 4
                    }
                ]
            },
            'intermediate': {
                'name': 'Intermediate Path',
                'description': 'Build on your foundation',
                'estimated_weeks': 12,
                'lessons': [
                    {
                        'id': 'int_1',
                        'title': 'Ser vs Estar Mastery',
                        'description': 'Master the two "to be" verbs',
                        'topics': ['ser uses', 'estar uses', 'common mistakes'],
                        'activities': ['grammar_exercises', 'quiz'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'int_2',
                        'title': 'Preterite Tense',
                        'description': 'Talk about completed past actions',
                        'topics': ['regular preterite', 'irregular verbs', 'time expressions'],
                        'activities': ['conjugation_practice', 'storytelling'],
                        'estimated_hours': 5
                    },
                    {
                        'id': 'int_3',
                        'title': 'Imperfect Tense',
                        'description': 'Describe past habits and ongoing actions',
                        'topics': ['imperfect formation', 'vs preterite', 'childhood stories'],
                        'activities': ['conjugation_practice', 'writing'],
                        'estimated_hours': 5
                    },
                    {
                        'id': 'int_4',
                        'title': 'Direct & Indirect Objects',
                        'description': 'Use object pronouns correctly',
                        'topics': ['direct objects', 'indirect objects', 'combining'],
                        'activities': ['grammar_exercises', 'conversation'],
                        'estimated_hours': 4
                    },
                    {
                        'id': 'int_5',
                        'title': 'Reflexive Verbs',
                        'description': 'Actions you do to yourself',
                        'topics': ['reflexive pronouns', 'daily routine', 'placement'],
                        'activities': ['conjugation_practice', 'conversation'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'int_6',
                        'title': 'Por vs Para',
                        'description': 'Master these tricky prepositions',
                        'topics': ['por uses', 'para uses', 'practice'],
                        'activities': ['grammar_exercises', 'translation'],
                        'estimated_hours': 4
                    },
                    {
                        'id': 'int_7',
                        'title': 'Future Tense',
                        'description': 'Talk about future plans',
                        'topics': ['future formation', 'irregular futures', 'ir + a + infinitive'],
                        'activities': ['conjugation_practice', 'conversation'],
                        'estimated_hours': 3
                    },
                    {
                        'id': 'int_8',
                        'title': 'Conditional Tense',
                        'description': 'Express hypotheticals and wishes',
                        'topics': ['conditional formation', 'polite requests', 'wishes'],
                        'activities': ['grammar_exercises', 'role-play'],
                        'estimated_hours': 3
                    }
                ]
            },
            'advanced': {
                'name': 'Advanced Path',
                'description': 'Achieve fluency',
                'estimated_weeks': 16,
                'lessons': [
                    {
                        'id': 'adv_1',
                        'title': 'Present Subjunctive',
                        'description': 'Express doubt, wishes, and emotions',
                        'topics': ['subjunctive formation', 'trigger phrases', 'WEIRDO'],
                        'activities': ['grammar_exercises', 'writing'],
                        'estimated_hours': 6
                    },
                    {
                        'id': 'adv_2',
                        'title': 'Imperfect Subjunctive',
                        'description': 'Past subjunctive mood',
                        'topics': ['formation', 'si clauses', 'wishes'],
                        'activities': ['grammar_exercises', 'conversation'],
                        'estimated_hours': 6
                    },
                    {
                        'id': 'adv_3',
                        'title': 'Perfect Tenses',
                        'description': 'Present perfect and beyond',
                        'topics': ['present perfect', 'past perfect', 'future perfect'],
                        'activities': ['conjugation_practice', 'storytelling'],
                        'estimated_hours': 5
                    },
                    {
                        'id': 'adv_4',
                        'title': 'Advanced Pronouns',
                        'description': 'Master all pronoun types',
                        'topics': ['demonstrative', 'possessive', 'indefinite', 'relative'],
                        'activities': ['grammar_exercises', 'translation'],
                        'estimated_hours': 4
                    },
                    {
                        'id': 'adv_5',
                        'title': 'Advanced Conversation',
                        'description': 'Discuss complex topics',
                        'topics': ['politics', 'culture', 'philosophy', 'debate'],
                        'activities': ['conversation', 'debate'],
                        'estimated_hours': 8
                    }
                ]
            }
        }
    
    def get_path(self, level):
        """Get learning path for a level"""
        return self.paths.get(level)
    
    def get_all_paths(self):
        """Get all available paths"""
        return {
            level: {
                'name': path['name'],
                'description': path['description'],
                'estimated_weeks': path['estimated_weeks'],
                'total_lessons': len(path['lessons'])
            }
            for level, path in self.paths.items()
        }
    
    def get_user_progress(self, user_id, path_name):
        """Get user's progress in a learning path"""
        cursor = self.conn.cursor()
        
        # Get completed lessons
        cursor.execute("""
            SELECT lesson_id, completed_at 
            FROM learning_progress 
            WHERE user_id = ? AND path_name = ? AND completed = 1
        """, (user_id, path_name))
        
        completed = [dict(row) for row in cursor.fetchall()]
        completed_ids = [row['lesson_id'] for row in completed]
        
        # Get path info
        path = self.paths.get(path_name)
        if not path:
            return None
        
        total_lessons = len(path['lessons'])
        completed_count = len(completed_ids)
        progress_percent = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0
        
        # Find next lesson
        next_lesson = None
        for lesson in path['lessons']:
            if lesson['id'] not in completed_ids:
                next_lesson = lesson
                break
        
        return {
            'path_name': path_name,
            'path_title': path['name'],
            'total_lessons': total_lessons,
            'completed_lessons': completed_count,
            'progress_percent': progress_percent,
            'completed_lesson_ids': completed_ids,
            'next_lesson': next_lesson,
            'estimated_weeks': path['estimated_weeks']
        }
    
    def complete_lesson(self, user_id, path_name, lesson_id):
        """Mark a lesson as completed"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO learning_progress 
            (user_id, path_name, lesson_id, completed, completed_at)
            VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, path_name, lesson_id)
            DO UPDATE SET completed = 1, completed_at = CURRENT_TIMESTAMP
        """, (user_id, path_name, lesson_id))
        
        self.conn.commit()
        
        # Check if user completed the path
        progress = self.get_user_progress(user_id, path_name)
        if progress['progress_percent'] == 100:
            return {'completed_path': True, 'progress': progress}
        
        return {'completed_path': False, 'progress': progress}
    
    def get_lesson_details(self, path_name, lesson_id):
        """Get detailed information about a specific lesson"""
        path = self.paths.get(path_name)
        if not path:
            return None
        
        for lesson in path['lessons']:
            if lesson['id'] == lesson_id:
                return lesson
        
        return None


# Test
if __name__ == '__main__':
    print("Testing Learning Paths...")
    from database import init_db
    
    init_db()
    lp = LearningPaths()
    
    # Get all paths
    paths = lp.get_all_paths()
    print("\nAvailable Paths:")
    for level, info in paths.items():
        print(f"  {info['name']}: {info['total_lessons']} lessons ({info['estimated_weeks']} weeks)")
    
    # Get beginner path
    beginner = lp.get_path('beginner')
    print(f"\nBeginner Path Lessons:")
    for i, lesson in enumerate(beginner['lessons'][:3], 1):
        print(f"  {i}. {lesson['title']} ({lesson['estimated_hours']}h)")
    
    # Test progress tracking
    user_id = 1
    lp.complete_lesson(user_id, 'beginner', 'beg_1')
    lp.complete_lesson(user_id, 'beginner', 'beg_2')
    
    progress = lp.get_user_progress(user_id, 'beginner')
    print(f"\nUser Progress:")
    print(f"  Completed: {progress['completed_lessons']}/{progress['total_lessons']}")
    print(f"  Progress: {progress['progress_percent']}%")
    if progress['next_lesson']:
        print(f"  Next: {progress['next_lesson']['title']}")
