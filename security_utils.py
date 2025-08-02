"""
Security Utilities - Password analysis and security functions
"""

import re
import math
from typing import Dict, List, Any
from collections import Counter

class PasswordAnalyzer:
    """Password security analyzer"""
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.common_patterns = [
            r'123456', r'password', r'admin', r'qwerty', r'abc',
            r'111111', r'welcome', r'login', r'master', r'secret'
        ]
        
    def _load_common_passwords(self) -> List[str]:
        """Load common passwords list"""
        # Top 100 most common passwords
        return [
            "password", "123456", "password123", "admin", "qwerty123",
            "123456789", "welcome", "monkey", "1234567890", "qwerty",
            "abc123", "111111", "12345678", "internet", "service",
            "welcome123", "zxcvbnm", "username", "login", "master",
            "hello", "guest", "administrator", "root", "system",
            "letmein", "pass", "secret", "default", "access"
        ]
        
    def analyze_strength(self, password: str) -> Dict[str, Any]:
        """
        Analyze password strength
        
        Returns:
            Dictionary with strength analysis results
        """
        if not password:
            return {'score': 0, 'level': 'Very Weak', 'feedback': ['Password is empty']}
            
        analysis = {
            'length': len(password),
            'character_sets': self._analyze_character_sets(password),
            'entropy': self._calculate_entropy(password),
            'patterns': self._check_patterns(password),
            'common_check': self._check_common_passwords(password),
            'repetition': self._check_repetition(password),
            'sequence': self._check_sequences(password)
        }
        
        # Calculate overall score
        score = self._calculate_score(analysis)
        level = self._get_strength_level(score)
        feedback = self._generate_feedback(analysis)
        
        return {
            'score': min(100, max(0, score)),
            'level': level,
            'feedback': feedback,
            'details': analysis
        }
        
    def _analyze_character_sets(self, password: str) -> Dict[str, int]:
        """Analyze character set usage"""
        sets = {
            'lowercase': len([c for c in password if c.islower()]),
            'uppercase': len([c for c in password if c.isupper()]),
            'digits': len([c for c in password if c.isdigit()]),
            'special': len([c for c in password if not c.isalnum()]),
            'unique_chars': len(set(password))
        }
        
        sets['total_sets'] = sum(1 for count in sets.values() if count > 0) - 1  # Exclude unique_chars
        
        return sets
        
    def _calculate_entropy(self, password: str) -> float:
        """Calculate password entropy"""
        if not password:
            return 0.0
            
        # Determine character set size
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(not c.isalnum() for c in password):
            charset_size += 32  # Approximate special characters
            
        if charset_size == 0:
            return 0.0
            
        # Calculate entropy
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)
        
    def _check_patterns(self, password: str) -> List[str]:
        """Check for common patterns"""
        patterns_found = []
        
        # Check for common password patterns
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                patterns_found.append(f"Contains common pattern: {pattern}")
                
        # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', 'abcd']
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                patterns_found.append(f"Contains keyboard pattern: {pattern}")
                
        # Check for date patterns
        date_pattern = r'\d{4}|\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}'
        if re.search(date_pattern, password):
            patterns_found.append("Contains date pattern")
            
        return patterns_found
        
    def _check_common_passwords(self, password: str) -> bool:
        """Check if password is in common passwords list"""
        return password.lower() in [cp.lower() for cp in self.common_passwords]
        
    def _check_repetition(self, password: str) -> Dict[str, Any]:
        """Check for character repetition"""
        if not password:
            return {'max_repeat': 0, 'repeated_chars': []}
            
        char_counts = Counter(password)
        max_repeat = max(char_counts.values()) if char_counts else 0
        repeated_chars = [char for char, count in char_counts.items() if count > 2]
        
        return {
            'max_repeat': max_repeat,
            'repeated_chars': repeated_chars,
            'repetition_ratio': max_repeat / len(password) if password else 0
        }
        
    def _check_sequences(self, password: str) -> List[str]:
        """Check for character sequences"""
        sequences_found = []
        
        if len(password) < 3:
            return sequences_found
            
        # Check for ascending sequences
        for i in range(len(password) - 2):
            if (ord(password[i]) + 1 == ord(password[i + 1]) and 
                ord(password[i + 1]) + 1 == ord(password[i + 2])):
                sequences_found.append(f"Ascending sequence: {password[i:i+3]}")
                
        # Check for descending sequences
        for i in range(len(password) - 2):
            if (ord(password[i]) - 1 == ord(password[i + 1]) and 
                ord(password[i + 1]) - 1 == ord(password[i + 2])):
                sequences_found.append(f"Descending sequence: {password[i:i+3]}")
                
        return sequences_found
        
    def _calculate_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall password score"""
        score = 0
        
        # Length score (0-30 points)
        length = analysis['length']
        if length >= 12:
            score += 30
        elif length >= 8:
            score += 20
        elif length >= 6:
            score += 10
        elif length >= 4:
            score += 5
            
        # Character set diversity (0-25 points)
        char_sets = analysis['character_sets']
        score += char_sets['total_sets'] * 6
        if char_sets['total_sets'] >= 4:
            score += 5  # Bonus for using all character types
            
        # Entropy score (0-25 points)
        entropy = analysis['entropy']
        if entropy >= 60:
            score += 25
        elif entropy >= 40:
            score += 20
        elif entropy >= 28:
            score += 15
        elif entropy >= 20:
            score += 10
        elif entropy >= 10:
            score += 5
            
        # Unique characters (0-10 points)
        unique_ratio = char_sets['unique_chars'] / length if length > 0 else 0
        score += int(unique_ratio * 10)
        
        # Penalties
        if analysis['common_check']:
            score -= 40
            
        if analysis['patterns']:
            score -= len(analysis['patterns']) * 5
            
        repetition = analysis['repetition']
        if repetition['max_repeat'] > 3:
            score -= (repetition['max_repeat'] - 3) * 5
            
        if analysis['sequence']:
            score -= len(analysis['sequence']) * 5
            
        return max(0, min(100, score))
        
    def _get_strength_level(self, score: int) -> str:
        """Get strength level based on score"""
        if score >= 90:
            return "Very Strong"
        elif score >= 75:
            return "Strong"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        elif score >= 20:
            return "Weak"
        else:
            return "Very Weak"
            
    def _generate_feedback(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement feedback"""
        feedback = []
        
        length = analysis['length']
        char_sets = analysis['character_sets']
        
        # Length feedback
        if length < 8:
            feedback.append("Use at least 8 characters")
        elif length < 12:
            feedback.append("Consider using 12 or more characters")
            
        # Character set feedback
        if char_sets['lowercase'] == 0:
            feedback.append("Add lowercase letters")
        if char_sets['uppercase'] == 0:
            feedback.append("Add uppercase letters")
        if char_sets['digits'] == 0:
            feedback.append("Add numbers")
        if char_sets['special'] == 0:
            feedback.append("Add special characters")
            
        # Pattern feedback
        if analysis['common_check']:
            feedback.append("Avoid common passwords")
            
        if analysis['patterns']:
            feedback.append("Avoid predictable patterns")
            
        # Repetition feedback
        repetition = analysis['repetition']
        if repetition['max_repeat'] > 3:
            feedback.append("Reduce character repetition")
            
        # Sequence feedback
        if analysis['sequence']:
            feedback.append("Avoid character sequences")
            
        if not feedback:
            feedback.append("Excellent password strength!")
            
        return feedback
        
    def full_analysis(self, password: str) -> str:
        """Generate full text analysis report"""
        analysis = self.analyze_strength(password)
        
        report = f"""
PASSWORD STRENGTH ANALYSIS REPORT
{'=' * 50}

Password Length: {analysis['details']['length']} characters
Overall Score: {analysis['score']}/100
Strength Level: {analysis['level']}

CHARACTER SET ANALYSIS:
• Lowercase letters: {analysis['details']['character_sets']['lowercase']}
• Uppercase letters: {analysis['details']['character_sets']['uppercase']}
• Numbers: {analysis['details']['character_sets']['digits']}
• Special characters: {analysis['details']['character_sets']['special']}
• Unique characters: {analysis['details']['character_sets']['unique_chars']}
• Character sets used: {analysis['details']['character_sets']['total_sets']}/4

SECURITY METRICS:
• Entropy: {analysis['details']['entropy']} bits
• Common password: {'Yes' if analysis['details']['common_check'] else 'No'}
• Maximum character repetition: {analysis['details']['repetition']['max_repeat']}

PATTERN ANALYSIS:
"""
        
        if analysis['details']['patterns']:
            for pattern in analysis['details']['patterns']:
                report += f"⚠ {pattern}\n"
        else:
            report += "✓ No common patterns detected\n"
            
        if analysis['details']['sequence']:
            report += "\nSEQUENCE ANALYSIS:\n"
            for sequence in analysis['details']['sequence']:
                report += f"⚠ {sequence}\n"
        else:
            report += "\n✓ No character sequences detected\n"
            
        report += f"\nRECOMMENDATIONS:\n"
        for i, feedback in enumerate(analysis['feedback'], 1):
            report += f"{i}. {feedback}\n"
            
        # Time to crack estimation
        entropy = analysis['details']['entropy']
        if entropy > 0:
            combinations = 2 ** entropy
            # Assuming 1 billion guesses per second
            seconds_to_crack = combinations / 2 / 1_000_000_000
            
            if seconds_to_crack > 365 * 24 * 3600:  # More than a year
                years = seconds_to_crack / (365 * 24 * 3600)
                if years > 1_000_000:
                    time_estimate = f"{years:.2e} years"
                else:
                    time_estimate = f"{years:.0f} years"
            elif seconds_to_crack > 24 * 3600:  # More than a day
                days = seconds_to_crack / (24 * 3600)
                time_estimate = f"{days:.0f} days"
            elif seconds_to_crack > 3600:  # More than an hour
                hours = seconds_to_crack / 3600
                time_estimate = f"{hours:.0f} hours"
            elif seconds_to_crack > 60:  # More than a minute
                minutes = seconds_to_crack / 60
                time_estimate = f"{minutes:.0f} minutes"
            else:
                time_estimate = f"{seconds_to_crack:.0f} seconds"
                
            report += f"\nCRACKING TIME ESTIMATE:\n"
            report += f"Time to crack (brute force): {time_estimate}\n"
            report += f"(Assuming 1 billion guesses per second)\n"
            
        return report


class SecurityUtils:
    """Additional security utilities"""
    
    @staticmethod
    def check_password_policy(password: str, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Check password against a security policy"""
        results = {
            'compliant': True,
            'violations': []
        }
        
        # Check minimum length
        min_length = policy.get('min_length', 8)
        if len(password) < min_length:
            results['compliant'] = False
            results['violations'].append(f"Password must be at least {min_length} characters")
            
        # Check maximum length
        max_length = policy.get('max_length', 128)
        if len(password) > max_length:
            results['compliant'] = False
            results['violations'].append(f"Password cannot exceed {max_length} characters")
            
        # Check required character types
        if policy.get('require_uppercase', False):
            if not any(c.isupper() for c in password):
                results['compliant'] = False
                results['violations'].append("Password must contain uppercase letters")
                
        if policy.get('require_lowercase', False):
            if not any(c.islower() for c in password):
                results['compliant'] = False
                results['violations'].append("Password must contain lowercase letters")
                
        if policy.get('require_numbers', False):
            if not any(c.isdigit() for c in password):
                results['compliant'] = False
                results['violations'].append("Password must contain numbers")
                
        if policy.get('require_special', False):
            if not any(not c.isalnum() for c in password):
                results['compliant'] = False
                results['violations'].append("Password must contain special characters")
                
        # Check forbidden patterns
        forbidden_patterns = policy.get('forbidden_patterns', [])
        for pattern in forbidden_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                results['compliant'] = False
                results['violations'].append(f"Password contains forbidden pattern: {pattern}")
                
        return results
