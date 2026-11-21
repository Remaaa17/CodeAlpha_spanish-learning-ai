"""
Learning Path API Routes
"""

from flask import Blueprint, request, jsonify
from backend.services.learning_paths import LearningPaths
from backend.services.gamification import GamificationSystem

path_bp = Blueprint('path', __name__, url_prefix='/api/path')

learning_paths = LearningPaths()
gamification = GamificationSystem()

@path_bp.route('/all', methods=['GET'])
def get_all_paths():
    """Get all learning paths"""
    try:
        paths = learning_paths.get_all_paths()
        
        return jsonify({
            'success': True,
            'paths': paths
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@path_bp.route('/details/<path_name>', methods=['GET'])
def get_path_details(path_name):
    """Get detailed path information"""
    try:
        path = learning_paths.get_path(path_name)
        
        if not path:
            return jsonify({'error': 'Path not found'}), 404
        
        return jsonify({
            'success': True,
            'path': path
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@path_bp.route('/progress', methods=['GET'])
def get_progress():
    """Get user progress in path"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        path_name = request.args.get('path_name', 'beginner')
        
        progress = learning_paths.get_user_progress(user_id, path_name)
        
        return jsonify({
            'success': True,
            'progress': progress
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@path_bp.route('/lesson/<lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get lesson details"""
    try:
        path_name = request.args.get('path_name', 'beginner')
        
        lesson = learning_paths.get_lesson_details(path_name, lesson_id)
        
        if not lesson:
            return jsonify({'error': 'Lesson not found'}), 404
        
        return jsonify({
            'success': True,
            'lesson': lesson
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@path_bp.route('/complete', methods=['POST'])
def complete_lesson():
    """Mark lesson as complete"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        path_name = data.get('path_name')
        lesson_id = data.get('lesson_id')
        
        if not path_name or not lesson_id:
            return jsonify({'error': 'path_name and lesson_id required'}), 400
        
        result = learning_paths.complete_lesson(user_id, path_name, lesson_id)
        
        # Award points
        gamification.award_points(user_id, 'lesson_completed')
        
        # Check badges
        progress = result['progress']
        if progress['completed_lessons'] == 1:
            gamification.award_badge(user_id, 'first_steps')
        
        if result['completed_path']:
            gamification.award_points(user_id, 'path_completed')
            gamification.award_badge(user_id, 'path_completer')
            
            if path_name == 'beginner':
                gamification.award_badge(user_id, 'beginner_graduate')
            elif path_name == 'intermediate':
                gamification.award_badge(user_id, 'intermediate_graduate')
            elif path_name == 'advanced':
                gamification.award_badge(user_id, 'advanced_graduate')
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
