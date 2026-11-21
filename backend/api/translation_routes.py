"""
Translation API Routes
"""

from flask import Blueprint, request, jsonify
from backend.services.translation_service import translate_text
from backend.models.database import get_db

translation_bp = Blueprint('translation', __name__, url_prefix='/api/translation')

@translation_bp.route('/translate', methods=['POST'])
def translate():
    """Translate text endpoint"""
    try:
        data = request.json
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'es')
        user_id = data.get('user_id')  # Optional
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Translate
        translated = translate_text(text, source_lang, target_lang)
        
        # Save to history if user_id provided
        if user_id:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO translation_history 
                (user_id, source_text, translated_text, source_lang, target_lang)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, text, translated, source_lang, target_lang))
            conn.commit()
        
        return jsonify({
            'success': True,
            'translated_text': translated,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@translation_bp.route('/history', methods=['GET'])
def get_history():
    """Get translation history for user"""
    try:
        user_id = request.args.get('user_id')
        limit = request.args.get('limit', 20, type=int)
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, source_text, translated_text, source_lang, target_lang, 
                   is_favorite, created_at
            FROM translation_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        history = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'success': True,
            'history': history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@translation_bp.route('/favorite', methods=['POST'])
def toggle_favorite():
    """Toggle favorite status of translation"""
    try:
        data = request.json
        translation_id = data.get('translation_id')
        is_favorite = data.get('is_favorite', True)
        
        if not translation_id:
            return jsonify({'error': 'translation_id required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE translation_history
            SET is_favorite = ?
            WHERE id = ?
        """, (is_favorite, translation_id))
        conn.commit()
        
        return jsonify({
            'success': True,
            'is_favorite': is_favorite
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
