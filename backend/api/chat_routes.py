"""
Chatbot API Routes
"""

from flask import Blueprint, request, jsonify
from backend.services.enhanced_chatbot import EnhancedChatbot
from backend.models.database import get_db
from backend.config.settings import GROQ_API_KEY

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Initialize chatbot
chatbot = EnhancedChatbot(groq_api_key=GROQ_API_KEY)

@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Send message to chatbot"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        user_id = data.get('user_id')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response
        response = chatbot.get_response(message, session_id)
        
        # Save to database if user_id provided
        if user_id:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations 
                (user_id, session_id, message, response)
                VALUES (?, ?, ?, ?)
            """, (user_id, session_id, message, response['response']))
            conn.commit()
        
        return jsonify({
            'success': True,
            'response': response['response'],
            'source': response['source'],
            'confidence': response['confidence']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        session_id = request.args.get('session_id', 'default')
        
        history = chatbot.get_conversation_history(session_id)
        
        return jsonify({
            'success': True,
            'history': history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        chatbot.clear_conversation(session_id)
        
        return jsonify({
            'success': True,
            'message': 'History cleared'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/faqs', methods=['GET'])
def get_faqs():
    """Get all FAQs"""
    try:
        faqs = chatbot.get_all_faqs()
        
        return jsonify({
            'success': True,
            'faqs': faqs
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
