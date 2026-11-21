"""
Spanish Learning AI Assistant - Main Application
Clean Architecture with Modular Design
"""

from flask import Flask, render_template
from flask_cors import CORS
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.config.settings import SECRET_KEY, DEBUG, CORS_ORIGINS
from backend.models.database import init_db
from backend.api.translation_routes import translation_bp
from backend.api.chat_routes import chat_bp
from backend.api.flashcard_routes import flashcard_bp
from backend.api.quiz_routes import quiz_bp
from backend.api.path_routes import path_bp
from backend.api.gamification_routes import gamification_bp
from backend.api.visual_learning_routes import visual_bp

# Create Flask app
app = Flask(__name__, 
            template_folder='frontend/pages',
            static_folder='frontend/assets')

# Configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Enable CORS
CORS(app, origins=CORS_ORIGINS)

# Register blueprints (API routes)
app.register_blueprint(translation_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(flashcard_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(path_bp)
app.register_blueprint(gamification_bp)
app.register_blueprint(visual_bp)

# Initialize database
init_db()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'version': '2.0.0',
        'features': {
            'translation': True,
            'chatbot': True,
            'flashcards': True,
            'quizzes': True,
            'learning_paths': True,
            'gamification': True,
            'visual_learning': True,
            'object_detection': True,
            'object_tracking': True
        },
        'models': {
            'yolo': 'YOLOv8 Nano',
            'tracker': 'Deep SORT',
            'nlp': 'NLTK + Groq AI'
        }
    }

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return {'error': 'Route not found'}, 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    print("🇪🇸 Spanish Learning AI Assistant")
    print("=" * 50)
    print("📝 Translation API: ✓")
    print("💬 NLP Chatbot: ✓")
    print("🃏 Flashcard System: ✓")
    print("📊 Quiz System: ✓")
    print("📚 Learning Paths: ✓")
    print("🎮 Gamification: ✓")
    print("🎥 Visual Learning (YOLO + Deep SORT): ✓")
    print("=" * 50)
    print("🌐 Server running on: http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000/health")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
