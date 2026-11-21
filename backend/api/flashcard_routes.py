"""
Flashcard API Routes
"""

from flask import Blueprint, request, jsonify
from backend.services.flashcard_system import FlashcardSystem
from backend.services.gamification import GamificationSystem

flashcard_bp = Blueprint('flashcard', __name__, url_prefix='/api/flashcard')

flashcard_system = FlashcardSystem()
gamification = GamificationSystem()

@flashcard_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all flashcard categories"""
    try:
        categories = flashcard_system.get_categories()
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flashcard_bp.route('/due', methods=['GET'])
def get_due_cards():
    """Get due cards for review"""
    try:
        user_id = request.args.get('user_id', type=int)
        limit = request.args.get('limit', 10, type=int)
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        cards = flashcard_system.get_due_cards(user_id, limit)
        
        return jsonify({
            'success': True,
            'cards': cards
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flashcard_bp.route('/practice', methods=['GET'])
def get_practice_session():
    """Get practice session"""
    try:
        user_id = request.args.get('user_id', type=int)
        count = request.args.get('count', 10, type=int)
        category = request.args.get('category')
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        cards = flashcard_system.get_practice_session(user_id, count, category)
        
        return jsonify({
            'success': True,
            'cards': cards
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flashcard_bp.route('/review', methods=['POST'])
def review_card():
    """Record flashcard review"""
    try:
        data = request.json
        user_id = data.get('user_id')
        flashcard_id = data.get('flashcard_id')
        correct = data.get('correct', False)
        
        if not user_id or not flashcard_id:
            return jsonify({'error': 'user_id and flashcard_id required'}), 400
        
        result = flashcard_system.record_review(user_id, flashcard_id, correct)
        
        # Award points
        if correct:
            gamification.award_points(user_id, 'flashcard_correct')
        else:
            gamification.award_points(user_id, 'flashcard_incorrect')
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flashcard_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get user flashcard statistics"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        stats = flashcard_system.get_user_stats(user_id)
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
