"""
Password Core - Core password generation functionality
"""

import secrets
import string
import random
from typing import Dict, List, Any

class PasswordGenerator:
    """Core password generation class"""
    
    def __init__(self):
        self.default_options = {
            'length': 16,
            'uppercase': True,
            'lowercase': True,
            'numbers': True,
            'symbols': True,
            'exclude_similar': False,
            'custom_chars': ''
        }
        
        # Character sets
        self.uppercase_chars = string.ascii_uppercase
        self.lowercase_chars = string.ascii_lowercase
        self.number_chars = string.digits
        self.symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.similar_chars = "0O1lI"
        
    def generate(self, options: Dict[str, Any] = None) -> str:
        """
        Generate a password based on specified options
        
        Args:
            options: Dictionary containing generation options
            
        Returns:
            Generated password string
        """
        if options is None:
            options = self.default_options.copy()
            
        # Merge with defaults
        final_options = {**self.default_options, **options}
        
        # Validate options
        self._validate_options(final_options)
        
        # Build character set
        charset = self._build_charset(final_options)
        
        if not charset:
            raise ValueError("No character types selected for password generation")
            
        # Generate password
        password = self._generate_password(charset, final_options)
        
        # Ensure password meets requirements
        password = self._ensure_requirements(password, final_options)
        
        return password
        
    def _validate_options(self, options: Dict[str, Any]):
        """Validate generation options"""
        length = options.get('length', 16)
        
        if not isinstance(length, int) or length < 1:
            raise ValueError("Password length must be a positive integer")
            
        if length > 1000:
            raise ValueError("Password length cannot exceed 1000 characters")
            
        # Check if at least one character type is selected
        char_types = ['uppercase', 'lowercase', 'numbers', 'symbols']
        if not any(options.get(char_type, False) for char_type in char_types):
            if not options.get('custom_chars', ''):
                raise ValueError("At least one character type must be selected")
                
    def _build_charset(self, options: Dict[str, Any]) -> str:
        """Build character set based on options"""
        charset = ""
        
        if options.get('uppercase', False):
            charset += self.uppercase_chars
            
        if options.get('lowercase', False):
            charset += self.lowercase_chars
            
        if options.get('numbers', False):
            charset += self.number_chars
            
        if options.get('symbols', False):
            charset += self.symbol_chars
            
        # Add custom characters
        custom_chars = options.get('custom_chars', '')
        if custom_chars:
            charset += custom_chars
            
        # Remove similar characters if requested
        if options.get('exclude_similar', False):
            charset = ''.join(c for c in charset if c not in self.similar_chars)
            
        # Remove duplicates while preserving order
        seen = set()
        charset = ''.join(c for c in charset if not (c in seen or seen.add(c)))
        
        return charset
        
    def _generate_password(self, charset: str, options: Dict[str, Any]) -> str:
        """Generate password from character set"""
        length = options['length']
        
        # Use cryptographically secure random generator
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        return password
        
    def _ensure_requirements(self, password: str, options: Dict[str, Any]) -> str:
        """Ensure password meets all requirements"""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            if self._check_requirements(password, options):
                return password
                
            # Regenerate if requirements not met
            charset = self._build_charset(options)
            password = self._generate_password(charset, options)
            attempts += 1
            
        # If we can't generate a compliant password, force compliance
        return self._force_compliance(password, options)
        
    def _check_requirements(self, password: str, options: Dict[str, Any]) -> bool:
        """Check if password meets all requirements"""
        # Check if password contains required character types
        if options.get('uppercase', False):
            if not any(c in self.uppercase_chars for c in password):
                return False
                
        if options.get('lowercase', False):
            if not any(c in self.lowercase_chars for c in password):
                return False
                
        if options.get('numbers', False):
            if not any(c in self.number_chars for c in password):
                return False
                
        if options.get('symbols', False):
            if not any(c in self.symbol_chars for c in password):
                return False
                
        return True
        
    def _force_compliance(self, password: str, options: Dict[str, Any]) -> str:
        """Force password to comply with requirements"""
        password_list = list(password)
        positions_to_replace = []
        
        # Collect required character types
        required_chars = []
        
        if options.get('uppercase', False):
            required_chars.append(secrets.choice(self.uppercase_chars))
            
        if options.get('lowercase', False):
            required_chars.append(secrets.choice(self.lowercase_chars))
            
        if options.get('numbers', False):
            required_chars.append(secrets.choice(self.number_chars))
            
        if options.get('symbols', False):
            required_chars.append(secrets.choice(self.symbol_chars))
            
        # Replace random positions with required characters
        for required_char in required_chars:
            if len(positions_to_replace) < len(password_list):
                pos = secrets.randbelow(len(password_list))
                while pos in positions_to_replace:
                    pos = secrets.randbelow(len(password_list))
                    
                password_list[pos] = required_char
                positions_to_replace.append(pos)
                
        return ''.join(password_list)
        
    def generate_multiple(self, count: int, options: Dict[str, Any] = None) -> List[str]:
        """Generate multiple passwords"""
        if count < 1 or count > 10000:
            raise ValueError("Count must be between 1 and 10000")
            
        passwords = []
        for _ in range(count):
            passwords.append(self.generate(options))
            
        return passwords
        
    def generate_memorable(self, word_count: int = 4, separator: str = "-") -> str:
        """Generate a memorable password using word combination"""
        # Simple word list for demonstration
        words = [
            "apple", "bridge", "canyon", "dolphin", "eagle", "forest", "garden", "harbor",
            "island", "jungle", "kayak", "lighthouse", "mountain", "ocean", "planet", "quartz",
            "river", "sunset", "tornado", "universe", "volcano", "waterfall", "zebra", "thunder"
        ]
        
        selected_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            # Capitalize first letter
            word = word.capitalize()
            selected_words.append(word)
            
        # Add numbers for security
        number = secrets.randbelow(1000)
        password = separator.join(selected_words) + str(number)
        
        return password
