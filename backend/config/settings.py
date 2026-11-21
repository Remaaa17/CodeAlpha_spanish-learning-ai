"""
Configuration Settings for Spanish Learning AI
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database
DATABASE_PATH = os.path.join(BASE_DIR, 'spanish_learning.db')

# Flask settings
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = False  # Disable debug mode to prevent auto-reload issues
SECRET_KEY = os.getenv('SECRET_KEY', 'spanish-learning-secret-key-change-in-production')

# API Keys (use environment variables)
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

# CORS settings
CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']

# Translation API
MYMEMORY_API_URL = 'https://api.mymemory.translated.net/get'
TRANSLATION_API_TIMEOUT = 10

# NLP Settings
NLP_SIMILARITY_THRESHOLD = 0.15
MAX_CONVERSATION_HISTORY = 20

# Flashcard Settings
SPACED_REPETITION_INTERVALS = {
    1: 1,   # 1 day after first correct
    2: 3,   # 3 days after second
    3: 7,   # 1 week after third
    4: 14,  # 2 weeks after fourth
    5: 30   # 1 month after fifth
}

# Gamification
POINTS = {
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

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
