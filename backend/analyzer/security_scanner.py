import re
from typing import List, Dict, Any


class SecurityScanner:
    """Scans code for security vulnerabilities"""
    
    VULNERABILITIES = {
        'sql_injection': {
            'patterns': [
                r'(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.+\s+(?:FROM|INTO|WHERE).*(?:\+|\.format|f["\'])',
                r'execute\s*\(\s*["\'].*\+',
                r'query\s*=\s*["\'].*\+',
            ],
            'cwe': 'CWE-89',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/89.html',
            'impact': 'An attacker can execute arbitrary SQL queries',
            'fix': 'Use parameterized queries or prepared statements'
        },
        'command_injection': {
            'patterns': [
                r'os\.system\s*\(["\'].*\+',
                r'subprocess\.(?:call|run|Popen)\s*\(["\'].*\+',
                r'system\s*\(["\'].*\+',
                r'exec\s*\(["\'].*\+',
            ],
            'cwe': 'CWE-78',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/78.html',
            'impact': 'An attacker can execute arbitrary system commands',
            'fix': 'Use safe subprocess APIs with list arguments or shell=False'
        },
        'xss': {
            'patterns': [
                r'innerHTML\s*=',
                r'dangerouslySetInnerHTML',
                r'document\.write\s*\(',
            ],
            'cwe': 'CWE-79',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/79.html',
            'impact': 'An attacker can inject malicious scripts',
            'fix': 'Use textContent instead of innerHTML or escape user input'
        },
        'hardcoded_secret': {
            'patterns': [
                r'(?:password|passwd|pwd)\s*[=:]\s*["\'][\w\-@#$%^&*]{6,}["\']',
                r'(?:api[_-]?key|apikey)\s*[=:]\s*["\'][\w\-]{20,}["\']',
                r'(?:secret|SECRET)\s*[=:]\s*["\'][\w\-]{20,}["\']',
                r'(?:token|TOKEN)\s*[=:]\s*["\'][\w\-]{20,}["\']',
                r'authorization:\s*["\']Bearer\s+[\w\-\.]+["\']',
            ],
            'cwe': 'CWE-798',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/798.html',
            'impact': 'Exposed credentials can be used to compromise the application',
            'fix': 'Use environment variables or a secrets management system'
        },
        'path_traversal': {
            'patterns': [
                r'open\s*\(\s*["\']\.\./',
                r'readFile\s*\(\s*["\']\.\./',
                r'os\.path\.join\s*\([^,]+\s*,\s*user_input',
            ],
            'cwe': 'CWE-22',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/22.html',
            'impact': 'An attacker can read arbitrary files from the system',
            'fix': 'Validate and sanitize file paths before use'
        },
        'weak_crypto': {
            'patterns': [
                r'MD5|SHA1|DES\(',
                r'crypto\.createCipher\(',
                r'hashlib\.md5\(',
            ],
            'cwe': 'CWE-326',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/326.html',
            'impact': 'Weak cryptographic algorithms are vulnerable to attacks',
            'fix': 'Use strong algorithms like SHA-256 or bcrypt'
        },
        'insecure_deserialization': {
            'patterns': [
                r'pickle\.load\(',
                r'yaml\.load\(',
                r'json\.loads\(',  # Only if unsafe
                r'unserialize\s*\(',
            ],
            'cwe': 'CWE-502',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/502.html',
            'impact': 'Deserialization of untrusted data can execute arbitrary code',
            'fix': 'Use safe deserialization methods or validate all input'
        },
        'unsafe_eval': {
            'patterns': [
                r'\beval\s*\(',
                r'\bexec\s*\(',
                r'\b__import__\s*\(',
            ],
            'cwe': 'CWE-95',
            'cwe_url': 'https://cwe.mitre.org/data/definitions/95.html',
            'impact': 'Arbitrary code execution vulnerability',
            'fix': 'Never use eval/exec with untrusted input. Use safer alternatives'
        },
    }
    
    def __init__(self, code: str, language: str):
        self.code = code
        self.language = language
        self.lines = code.split('\n')
        self.issues: List[Dict[str, Any]] = []
    
    def scan(self) -> List[Dict[str, Any]]:
        """Scan code for security vulnerabilities"""
        for vuln_type, config in self.VULNERABILITIES.items():
            self._scan_for_vulnerability(vuln_type, config)
        
        return self.issues
    
    def _scan_for_vulnerability(self, vuln_type: str, config: Dict[str, Any]):
        """Scan for a specific vulnerability type"""
        patterns = config['patterns']
        severity_map = {
            'sql_injection': 'critical',
            'command_injection': 'critical',
            'unsafe_eval': 'critical',
            'insecure_deserialization': 'critical',
            'hardcoded_secret': 'critical',
            'xss': 'high',
            'path_traversal': 'high',
            'weak_crypto': 'high',
        }
        
        for i, line in enumerate(self.lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issue_title = vuln_type.replace('_', ' ').title()
                    self.issues.append({
                        'type': 'security',
                        'severity': severity_map.get(vuln_type, 'medium'),
                        'category': issue_title,
                        'line_number': i,
                        'title': f'{issue_title} vulnerability detected',
                        'description': f'Potential {issue_title} vulnerability on line {i}',
                        'impact': config['impact'],
                        'suggested_fix': config['fix'],
                        'cwe': config['cwe'],
                        'cwe_url': config['cwe_url'],
                        'code_context': line.strip()
                    })
                    break  # Only report once per line
