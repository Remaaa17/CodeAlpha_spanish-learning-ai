"""
Gamification API Routes
"""

from flask import Blueprint, request, jsonify
from backend.services.gamification import GamificationSystem

gamification_bp = Blueprint('gamification', __name__, url_prefix='/api/gamification')

gamification = GamificationSystem()

@gamification_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get user gamification summary"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        summary = gamification.get_gamification_summary(user_id)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/badges', methods=['GET'])
def get_badges():
    """Get all badges with earned status"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        badges = gamification.get_all_badges_with_status(user_id)
        
        return jsonify({
            'success': True,
            'badges': badges
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard"""
    try:
        limit = request.args.get('limit', 10, type=int)
        timeframe = request.args.get('timeframe', 'all_time')
        
        leaderboard = gamification.get_leaderboard(limit, timeframe)
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/streak', methods=['POST'])
def update_streak():
    """Update user's daily streak"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        
        streak = gamification.update_streak(user_id)
        
        return jsonify({
            'success': True,
            'streak': streak
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
