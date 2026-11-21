"""
Quiz API Routes
"""

from flask import Blueprint, request, jsonify
from backend.services.quiz_system import QuizSystem
from backend.services.gamification import GamificationSystem

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

quiz_system = QuizSystem()
gamification = GamificationSystem()

@quiz_bp.route('/generate', methods=['POST'])
def generate_quiz():
    """Generate a quiz"""
    try:
        data = request.json
        quiz_type = data.get('quiz_type', 'vocabulary')
        topic = data.get('topic', 'mixed')
        count = data.get('count', 10)
        category = data.get('category')
        
        if quiz_type == 'vocabulary':
            quiz = quiz_system.generate_vocabulary_quiz(category, count)
        elif quiz_type == 'conjugation':
            quiz = quiz_system.generate_conjugation_quiz(count)
        elif quiz_type == 'translation':
            direction = data.get('direction', 'es_to_en')
            quiz = quiz_system.generate_translation_quiz(direction, count)
        elif quiz_type == 'grammar':
            quiz = quiz_system.generate_grammar_quiz(topic, count)
        else:
            return jsonify({'error': 'Invalid quiz type'}), 400
        
        return jsonify({
            'success': True,
            'quiz': quiz
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/grade', methods=['POST'])
def grade_quiz():
    """Grade quiz answers"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        quiz_type = data.get('quiz_type')
        topic = data.get('topic', 'mixed')
        answers = data.get('answers', [])
        questions = data.get('questions', [])
        
        if not answers or not questions:
            return jsonify({'error': 'Answers and questions required'}), 400
        
        results = quiz_system.grade_quiz(user_id, quiz_type, topic, answers, questions)
        
        # Award points
        gamification.award_points(user_id, 'quiz_completed')
        if results['score'] == 100:
            gamification.award_points(user_id, 'quiz_perfect')
            gamification.award_badge(user_id, 'quiz_ace')
        
        # Check for quiz champion badge
        stats = quiz_system.get_quiz_stats(user_id)
        if stats['total_quizzes'] >= 20:
            gamification.award_badge(user_id, 'quiz_champion')
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/history', methods=['GET'])
def get_history():
    """Get quiz history"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        history = quiz_system.get_user_quiz_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'history': history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get quiz statistics"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        stats = quiz_system.get_quiz_stats(user_id)
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
