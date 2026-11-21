"""
Gamification System
Points, badges, streaks, and achievements
"""

from backend.models.database import get_db
from datetime import datetime, date, timedelta

class GamificationSystem:
    """
    Manage points, badges, streaks, and achievements
    """
    
    def __init__(self):
        self.conn = get_db()
        self.badges = self._define_badges()
        self.point_values = {
            'translation': 5,
            'chat_message': 2,
            'flashcard_correct': 10,
            'flashcard_incorrect': 2,
            'quiz_completed': 20,
            'quiz_perfect': 50,
            'lesson_completed': 30,
            'path_completed': 200,
            'daily_login': 10,
            'week_streak': 50,
            'month_streak': 200
        }
    
    def _define_badges(self):
        """Define all available badges"""
        return {
            'first_steps': {
                'name': 'First Steps',
                'description': '¡Bienvenido! Completed your first lesson',
                'icon': '👶',
                'criteria': 'complete_1_lesson'
            },
            'translator': {
                'name': 'Translator',
                'description': 'Translated 100 phrases',
                'icon': '🌐',
                'criteria': 'translate_100'
            },
            'conversation_starter': {
                'name': 'Conversation Starter',
                'description': 'Had 50 chat conversations',
                'icon': '💬',
                'criteria': 'chat_50'
            },
            'flashcard_novice': {
                'name': 'Flashcard Novice',
                'description': 'Reviewed 50 flashcards',
                'icon': '🃏',
                'criteria': 'flashcard_50'
            },
            'flashcard_master': {
                'name': 'Flashcard Master',
                'description': 'Mastered 100 flashcards',
                'icon': '🎯',
                'criteria': 'master_100'
            },
            'quiz_ace': {
                'name': 'Quiz Ace',
                'description': 'Scored 100% on a quiz',
                'icon': '🌟',
                'criteria': 'quiz_perfect'
            },
            'quiz_champion': {
                'name': 'Quiz Champion',
                'description': 'Completed 20 quizzes',
                'icon': '🏆',
                'criteria': 'quiz_20'
            },
            'streak_warrior': {
                'name': 'Streak Warrior',
                'description': '7-day learning streak',
                'icon': '🔥',
                'criteria': 'streak_7'
            },
            'streak_legend': {
                'name': 'Streak Legend',
                'description': '30-day learning streak',
                'icon': '⚡',
                'criteria': 'streak_30'
            },
            'dedicated_learner': {
                'name': 'Dedicated Learner',
                'description': 'Earned 1000 points',
                'icon': '💪',
                'criteria': 'points_1000'
            },
            'spanish_scholar': {
                'name': 'Spanish Scholar',
                'description': 'Earned 5000 points',
                'icon': '🎓',
                'criteria': 'points_5000'
            },
            'path_completer': {
                'name': 'Path Completer',
                'description': 'Completed a learning path',
                'icon': '🎖️',
                'criteria': 'complete_path'
            },
            'beginner_graduate': {
                'name': 'Beginner Graduate',
                'description': 'Completed Beginner Path',
                'icon': '🥉',
                'criteria': 'complete_beginner'
            },
            'intermediate_graduate': {
                'name': 'Intermediate Graduate',
                'description': 'Completed Intermediate Path',
                'icon': '🥈',
                'criteria': 'complete_intermediate'
            },
            'advanced_graduate': {
                'name': 'Advanced Graduate',
                'description': 'Completed Advanced Path',
                'icon': '🥇',
                'criteria': 'complete_advanced'
            }
        }
    
    def award_points(self, user_id, activity, amount=None):
        """Award points for an activity"""
        cursor = self.conn.cursor()
        
        # Get point value
        points = amount or self.point_values.get(activity, 0)
        
        # Update user points
        cursor.execute("""
            UPDATE users 
            SET points = points + ?
            WHERE id = ?
        """, (points, user_id))
        
        self.conn.commit()
        
        # Check for point-based badges
        self._check_point_badges(user_id)
        
        return points
    
    def get_user_points(self, user_id):
        """Get user's total points"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT points FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else 0
    
    def update_streak(self, user_id):
        """Update user's login streak"""
        cursor = self.conn.cursor()
        
        # Get last login
        cursor.execute("""
            SELECT last_login, streak_days 
            FROM users 
            WHERE id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        if not row:
            return 0
        
        last_login = row[0]
        current_streak = row[1] or 0
        
        today = date.today()
        
        if last_login:
            last_date = datetime.strptime(last_login, '%Y-%m-%d').date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                # Consecutive day
                new_streak = current_streak + 1
                self.award_points(user_id, 'daily_login')
            elif days_diff == 0:
                # Same day
                new_streak = current_streak
            else:
                # Streak broken
                new_streak = 1
        else:
            new_streak = 1
        
        # Update streak
        cursor.execute("""
            UPDATE users 
            SET streak_days = ?, last_login = ?
            WHERE id = ?
        """, (new_streak, today.isoformat(), user_id))
        
        self.conn.commit()
        
        # Check streak badges
        self._check_streak_badges(user_id, new_streak)
        
        return new_streak
    
    def _check_point_badges(self, user_id):
        """Check and award point-based badges"""
        points = self.get_user_points(user_id)
        
        if points >= 1000:
            self.award_badge(user_id, 'dedicated_learner')
        if points >= 5000:
            self.award_badge(user_id, 'spanish_scholar')
    
    def _check_streak_badges(self, user_id, streak):
        """Check and award streak badges"""
        if streak >= 7:
            self.award_badge(user_id, 'streak_warrior')
            self.award_points(user_id, 'week_streak')
        if streak >= 30:
            self.award_badge(user_id, 'streak_legend')
            self.award_points(user_id, 'month_streak')
    
    def award_badge(self, user_id, badge_key):
        """Award a badge to user"""
        cursor = self.conn.cursor()
        
        # Check if already has badge
        cursor.execute("""
            SELECT id FROM achievements 
            WHERE user_id = ? AND badge_name = ?
        """, (user_id, badge_key))
        
        if cursor.fetchone():
            return False  # Already has badge
        
        badge = self.badges.get(badge_key)
        if not badge:
            return False
        
        # Award badge
        cursor.execute("""
            INSERT INTO achievements 
            (user_id, badge_name, badge_description)
            VALUES (?, ?, ?)
        """, (user_id, badge_key, badge['description']))
        
        self.conn.commit()
        return True
    
    def get_user_badges(self, user_id):
        """Get all badges earned by user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT badge_name, earned_at 
            FROM achievements 
            WHERE user_id = ?
            ORDER BY earned_at DESC
        """, (user_id,))
        
        earned = cursor.fetchall()
        
        # Add badge details
        badges = []
        for row in earned:
            badge_key = row[0]
            if badge_key in self.badges:
                badge_info = self.badges[badge_key].copy()
                badge_info['earned_at'] = row[1]
                badge_info['key'] = badge_key
                badges.append(badge_info)
        
        return badges
    
    def get_all_badges_with_status(self, user_id):
        """Get all badges with earned status"""
        earned_keys = [b['key'] for b in self.get_user_badges(user_id)]
        
        all_badges = []
        for key, badge in self.badges.items():
            badge_info = badge.copy()
            badge_info['key'] = key
            badge_info['earned'] = key in earned_keys
            all_badges.append(badge_info)
        
        return all_badges
    
    def get_leaderboard(self, limit=10, timeframe='all_time'):
        """Get leaderboard"""
        cursor = self.conn.cursor()
        
        if timeframe == 'all_time':
            cursor.execute("""
                SELECT id, username, points, streak_days, level
                FROM users
                ORDER BY points DESC
                LIMIT ?
            """, (limit,))
        elif timeframe == 'week':
            # Points earned in last 7 days would need additional tracking
            # For now, use all-time
            cursor.execute("""
                SELECT id, username, points, streak_days, level
                FROM users
                ORDER BY points DESC
                LIMIT ?
            """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_user_rank(self, user_id):
        """Get user's rank on leaderboard"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) + 1
            FROM users u1
            JOIN users u2 ON u2.id = ?
            WHERE u1.points > u2.points
        """, (user_id,))
        
        rank = cursor.fetchone()[0]
        return rank
    
    def get_gamification_summary(self, user_id):
        """Get complete gamification summary for user"""
        cursor = self.conn.cursor()
        
        # Get user info
        cursor.execute("""
            SELECT username, points, streak_days, level
            FROM users
            WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            return None
        
        badges = self.get_user_badges(user_id)
        rank = self.get_user_rank(user_id)
        
        # Calculate level progress (100 points per level)
        current_points = user[1]
        current_level = current_points // 100
        points_to_next = 100 - (current_points % 100)
        
        return {
            'username': user[0],
            'points': user[1],
            'streak_days': user[2] or 0,
            'level': current_level,
            'points_to_next_level': points_to_next,
            'badges_earned': len(badges),
            'total_badges': len(self.badges),
            'recent_badges': badges[:5],
            'rank': rank
        }
    
    def check_activity_badges(self, user_id, activity_type, count):
        """Check and award activity-based badges"""
        if activity_type == 'translation' and count >= 100:
            self.award_badge(user_id, 'translator')
        elif activity_type == 'chat' and count >= 50:
            self.award_badge(user_id, 'conversation_starter')
        elif activity_type == 'flashcard' and count >= 50:
            self.award_badge(user_id, 'flashcard_novice')
        elif activity_type == 'flashcard_mastered' and count >= 100:
            self.award_badge(user_id, 'flashcard_master')
        elif activity_type == 'quiz' and count >= 20:
            self.award_badge(user_id, 'quiz_champion')
        elif activity_type == 'lesson' and count >= 1:
            self.award_badge(user_id, 'first_steps')


# Test
if __name__ == '__main__':
    print("Testing Gamification System...")
    from database import init_db
    
    init_db()
    
    # Create test user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, email, password_hash)
        VALUES ('test_user', 'test@example.com', 'hash')
    """)
    conn.commit()
    
    cursor.execute("SELECT id FROM users WHERE username = 'test_user'")
    user_id = cursor.fetchone()[0]
    
    gs = GamificationSystem()
    
    # Test awarding points
    gs.award_points(user_id, 'translation')
    gs.award_points(user_id, 'quiz_completed')
    gs.award_points(user_id, 'lesson_completed')
    
    points = gs.get_user_points(user_id)
    print(f"\nUser Points: {points}")
    
    # Test streak
    streak = gs.update_streak(user_id)
    print(f"Streak: {streak} days")
    
    # Test badges
    gs.award_badge(user_id, 'first_steps')
    gs.award_badge(user_id, 'translator')
    
    badges = gs.get_user_badges(user_id)
    print(f"\nBadges Earned: {len(badges)}")
    for badge in badges:
        print(f"  {badge['icon']} {badge['name']}: {badge['description']}")
    
    # Test summary
    summary = gs.get_gamification_summary(user_id)
    print(f"\nGamification Summary:")
    print(f"  Points: {summary['points']}")
    print(f"  Level: {summary['level']}")
    print(f"  Streak: {summary['streak_days']} days")
    print(f"  Badges: {summary['badges_earned']}/{summary['total_badges']}")
    print(f"  Rank: #{summary['rank']}")
