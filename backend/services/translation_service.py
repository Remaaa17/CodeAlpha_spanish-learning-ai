"""
Translation Service
Uses MyMemory Translation API (free, no dependencies)
Alternative: deep-translator for multiple API support
"""

import requests

# No initialization needed for MyMemory API

def translate_text(text, source_lang='en', target_lang='es'):
    """
    Translate text using MyMemory API (free, no key required)
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code (e.g., 'en', 'es')
        target_lang (str): Target language code
    
    Returns:
        str: Translated text
    """
    try:
        # Using MyMemory API directly
        return translate_mymemory(text, source_lang, target_lang)
    
    except Exception as e:
        print(f"Translation error: {e}")
        return f"Translation failed: {str(e)}"

def translate_mymemory(text, source_lang='en', target_lang='es'):
    """
    Fallback translation using MyMemory API (free, no key required)
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
    
    Returns:
        str: Translated text
    """
    url = f"https://api.mymemory.translated.net/get"
    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get('responseStatus') == 200 or data.get('responseData'):
        return data['responseData']['translatedText']
    else:
        raise Exception("Translation failed")

def detect_language(text):
    """
    Detect the language of the text
    
    Args:
        text (str): Text to detect
    
    Returns:
        str: Language code
    """
    try:
        # Simple detection based on common words (basic implementation)
        spanish_words = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese', 'la', 'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin', 'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo', 'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero', 'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella', 'sí', 'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa', 'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte', 'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar', 'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo', 'decir', 'mundo', 'país', 'contra', 'aquí', 'casa', 'último', 'salir', 'mientras']
        
        text_lower = text.lower()
        spanish_count = sum(1 for word in spanish_words if word in text_lower)
        
        # If many Spanish words found, likely Spanish
        if spanish_count > 3:
            return 'es'
        return 'en'
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'unknown'

# Test function
if __name__ == '__main__':
    # Test translations
    print("Testing translation service...")
    
    test_texts = [
        ("Hello, how are you?", "en", "es"),
        ("I am learning Spanish", "en", "es"),
        ("Hola, ¿cómo estás?", "es", "en")
    ]
    
    for text, src, tgt in test_texts:
        translated = translate_text(text, src, tgt)
        print(f"{text} -> {translated}")
