"""
Configuration settings for Password Generator
"""

# Application Configuration
APP_CONFIG = {
    'name': 'Advanced Password Generator',
    'version': '2.0.0',
    'author': 'OMM Projects',
    'description': 'Professional password generator with advanced features'
}

# Default Generation Settings
DEFAULT_GENERATION_SETTINGS = {
    'length': 16,
    'uppercase': True,
    'lowercase': True,
    'numbers': True,
    'symbols': True,
    'exclude_similar': False,
    'custom_chars': ''
}

# Security Policies
SECURITY_POLICIES = {
    'basic': {
        'min_length': 8,
        'max_length': 128,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special': False
    },
    'medium': {
        'min_length': 12,
        'max_length': 128,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special': True
    },
    'strict': {
        'min_length': 16,
        'max_length': 64,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special': True,
        'forbidden_patterns': [
            r'password', r'123456', r'qwerty', r'admin'
        ]
    }
}

# GUI Configuration
GUI_CONFIG = {
    'theme': 'dark',
    'colors': {
        'bg_primary': '#1a1a2e',
        'bg_secondary': '#16213e',
        'bg_tertiary': '#2a2a3e',
        'accent': '#00d4ff',
        'success': '#00ff88',
        'warning': '#ff8800',
        'error': '#ff4444',
        'text_primary': '#ffffff',
        'text_secondary': '#888888'
    },
    'fonts': {
        'default': ('Segoe UI', 10),
        'title': ('Segoe UI', 24, 'bold'),
        'mono': ('Courier New', 10),
        'button': ('Segoe UI', 10, 'bold')
    }
}

# File Paths
PATHS = {
    'settings': 'settings.json',
    'history': 'password_history.json',
    'logs': 'logs/',
    'exports': 'exports/',
    'assets': 'assets/'
}

# Export Formats
EXPORT_FORMATS = {
    'txt': {
        'extension': '.txt',
        'mime_type': 'text/plain',
        'description': 'Text File'
    },
    'csv': {
        'extension': '.csv', 
        'mime_type': 'text/csv',
        'description': 'CSV File'
    },
    'json': {
        'extension': '.json',
        'mime_type': 'application/json', 
        'description': 'JSON File'
    }
}

# Strength Levels
STRENGTH_LEVELS = {
    0: {'name': 'Very Weak', 'color': '#ff4444'},
    20: {'name': 'Weak', 'color': '#ff8800'},
    40: {'name': 'Fair', 'color': '#ffff00'},
    60: {'name': 'Good', 'color': '#88ff00'},
    80: {'name': 'Strong', 'color': '#00ff00'},
    90: {'name': 'Very Strong', 'color': '#00aa00'}
}
