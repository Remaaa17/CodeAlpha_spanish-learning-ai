"""
Database Models and Setup
SQLite database for user accounts, progress tracking, flashcards, etc.
"""

import sqlite3
import json
from datetime import datetime
import os

DATABASE_PATH = 'spanish_learning.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            level TEXT DEFAULT 'beginner',
            points INTEGER DEFAULT 0,
            streak_days INTEGER DEFAULT 0,
            last_login DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Translation history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            source_text TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            is_favorite BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Conversation history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Flashcards
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spanish_word TEXT NOT NULL,
            english_word TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT DEFAULT 'easy',
            example_sentence TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User flashcard progress
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcard_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            flashcard_id INTEGER NOT NULL,
            correct_count INTEGER DEFAULT 0,
            incorrect_count INTEGER DEFAULT 0,
            last_reviewed DATE,
            next_review DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (flashcard_id) REFERENCES flashcards(id),
            UNIQUE(user_id, flashcard_id)
        )
    ''')
    
    # Quiz results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_type TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            time_taken INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Learning path progress
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            path_name TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, path_name, lesson_id)
        )
    ''')
    
    # Achievements/Badges
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            badge_name TEXT NOT NULL,
            badge_description TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Expanded FAQ database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            keywords TEXT,
            difficulty TEXT DEFAULT 'beginner',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")

def seed_flashcards():
    """Seed initial flashcard data"""
    conn = get_db()
    cursor = conn.cursor()
    
    flashcards = [
        # Greetings
        ('Hola', 'Hello', 'greetings', 'easy', 'Hola, ¿cómo estás?'),
        ('Buenos días', 'Good morning', 'greetings', 'easy', 'Buenos días, señor.'),
        ('Buenas tardes', 'Good afternoon', 'greetings', 'easy', 'Buenas tardes, ¿cómo está?'),
        ('Buenas noches', 'Good evening', 'greetings', 'easy', 'Buenas noches, hasta mañana.'),
        ('Adiós', 'Goodbye', 'greetings', 'easy', 'Adiós, nos vemos pronto.'),
        
        # Common verbs
        ('Hablar', 'To speak', 'verbs', 'easy', 'Yo hablo español.'),
        ('Comer', 'To eat', 'verbs', 'easy', 'Ella come una manzana.'),
        ('Vivir', 'To live', 'verbs', 'easy', 'Nosotros vivimos en España.'),
        ('Ser', 'To be (permanent)', 'verbs', 'medium', 'Yo soy estudiante.'),
        ('Estar', 'To be (temporary)', 'verbs', 'medium', 'Estoy cansado.'),
        ('Tener', 'To have', 'verbs', 'easy', 'Tengo un perro.'),
        ('Hacer', 'To do/make', 'verbs', 'medium', '¿Qué haces?'),
        ('Ir', 'To go', 'verbs', 'medium', 'Voy al parque.'),
        ('Querer', 'To want', 'verbs', 'medium', 'Quiero aprender español.'),
        ('Poder', 'To be able to', 'verbs', 'medium', 'No puedo ir hoy.'),
        
        # Numbers
        ('Uno', 'One', 'numbers', 'easy', 'Tengo un libro.'),
        ('Dos', 'Two', 'numbers', 'easy', 'Dos personas.'),
        ('Tres', 'Three', 'numbers', 'easy', 'Tres días.'),
        ('Diez', 'Ten', 'numbers', 'easy', 'Diez dólares.'),
        ('Veinte', 'Twenty', 'numbers', 'easy', 'Veinte años.'),
        ('Cien', 'One hundred', 'numbers', 'easy', 'Cien por ciento.'),
        
        # Food
        ('Pan', 'Bread', 'food', 'easy', 'Quiero pan, por favor.'),
        ('Agua', 'Water', 'food', 'easy', 'Un vaso de agua.'),
        ('Manzana', 'Apple', 'food', 'easy', 'Como una manzana.'),
        ('Pollo', 'Chicken', 'food', 'easy', 'Pollo con arroz.'),
        ('Arroz', 'Rice', 'food', 'easy', 'Me gusta el arroz.'),
        ('Café', 'Coffee', 'food', 'easy', 'Un café con leche.'),
        ('Leche', 'Milk', 'food', 'easy', 'Leche fría.'),
        ('Queso', 'Cheese', 'food', 'easy', 'Queso español.'),
        ('Tomate', 'Tomato', 'food', 'easy', 'Ensalada de tomate.'),
        ('Pescado', 'Fish', 'food', 'easy', 'Pescado fresco.'),
        
        # Colors
        ('Rojo', 'Red', 'colors', 'easy', 'Un coche rojo.'),
        ('Azul', 'Blue', 'colors', 'easy', 'El cielo azul.'),
        ('Verde', 'Green', 'colors', 'easy', 'Una manzana verde.'),
        ('Amarillo', 'Yellow', 'colors', 'easy', 'El sol amarillo.'),
        ('Negro', 'Black', 'colors', 'easy', 'Un gato negro.'),
        ('Blanco', 'White', 'colors', 'easy', 'Nieve blanca.'),
        
        # Family
        ('Madre', 'Mother', 'family', 'easy', 'Mi madre es profesora.'),
        ('Padre', 'Father', 'family', 'easy', 'Mi padre trabaja.'),
        ('Hermano', 'Brother', 'family', 'easy', 'Tengo un hermano.'),
        ('Hermana', 'Sister', 'family', 'easy', 'Mi hermana menor.'),
        ('Abuelo', 'Grandfather', 'family', 'easy', 'Mi abuelo es amable.'),
        ('Abuela', 'Grandmother', 'family', 'easy', 'Visito a mi abuela.'),
        
        # Common phrases
        ('Por favor', 'Please', 'phrases', 'easy', 'Por favor, ayúdame.'),
        ('Gracias', 'Thank you', 'phrases', 'easy', 'Muchas gracias.'),
        ('De nada', 'You\'re welcome', 'phrases', 'easy', 'De nada, amigo.'),
        ('Lo siento', 'I\'m sorry', 'phrases', 'easy', 'Lo siento mucho.'),
        ('Perdón', 'Excuse me', 'phrases', 'easy', 'Perdón, señor.'),
        ('¿Cómo estás?', 'How are you?', 'phrases', 'easy', '¿Cómo estás hoy?'),
        ('Me llamo', 'My name is', 'phrases', 'easy', 'Me llamo María.'),
        ('Mucho gusto', 'Nice to meet you', 'phrases', 'easy', 'Mucho gusto, Juan.'),
    ]
    
    for card in flashcards:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO flashcards 
                (spanish_word, english_word, category, difficulty, example_sentence)
                VALUES (?, ?, ?, ?, ?)
            ''', card)
        except:
            pass  # Skip duplicates
    
    conn.commit()
    conn.close()
    print(f"✓ Seeded {len(flashcards)} flashcards")

# Initialize database on import
if not os.path.exists(DATABASE_PATH):
    init_db()
    seed_flashcards()
