import re
import ast
from typing import List, Dict, Any
from models import Issue


class StaticAnalyzer:
    """Performs static analysis on source code"""
    
    def __init__(self, code: str, language: str):
        self.code = code
        self.language = language
        self.lines = code.split('\n')
        self.issues: List[Dict[str, Any]] = []
    
    def analyze(self) -> List[Dict[str, Any]]:
        """Run all static analysis checks"""
        if self.language.lower() == 'python':
            self._analyze_python()
        elif self.language.lower() in ['javascript', 'typescript']:
            self._analyze_javascript()
        elif self.language.lower() == 'java':
            self._analyze_java()
        else:
            self._analyze_generic()
        
        return self.issues
    
    def _analyze_python(self):
        """Python-specific analysis using AST"""
        try:
            tree = ast.parse(self.code)
            
            # Check for common issues
            self._check_undefined_variables(tree)
            self._check_long_functions(tree)
            self._check_bare_except()
            self._check_dangerous_functions()
            self._check_division_by_zero(tree)
            self._check_uninitialized_variables(tree)
            
        except SyntaxError as e:
            self.issues.append({
                'type': 'bug',
                'severity': 'critical',
                'category': 'Syntax Error',
                'line_number': e.lineno or 1,
                'title': 'Syntax Error',
                'description': str(e.msg),
                'impact': 'Code will not run',
                'suggested_fix': 'Fix the syntax error'
            })
    
    def _check_undefined_variables(self, tree):
        """Check for potentially undefined variables"""
        class VariableChecker(ast.NodeVisitor):
            def __init__(self):
                self.defined_vars = set()
                self.issues = []
            
            def visit_FunctionDef(self, node):
                # Track function parameters as defined
                for arg in node.args.args:
                    self.defined_vars.add(arg.arg)
                self.generic_visit(node)
            
            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.defined_vars.add(target.id)
                self.generic_visit(node)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load) and node.id not in self.defined_vars:
                    if not node.id.isupper():  # Skip constants
                        self.issues.append({
                            'type': 'bug',
                            'severity': 'high',
                            'category': 'Undefined Variable',
                            'line_number': node.lineno,
                            'title': f'Undefined variable: {node.id}',
                            'description': f'Variable "{node.id}" may not be defined',
                            'impact': 'This will cause a NameError at runtime',
                            'suggested_fix': f'Define {node.id} before using it'
                        })
        
        checker = VariableChecker()
        checker.visit(tree)
        self.issues.extend(checker.issues)
    
    def _check_long_functions(self, tree):
        """Check for functions that are too long"""
        class FunctionLengthChecker(ast.NodeVisitor):
            def __init__(self, lines):
                self.issues = []
                self.lines = lines
            
            def visit_FunctionDef(self, node):
                # Count lines in function
                if hasattr(node, 'end_lineno'):
                    func_length = node.end_lineno - node.lineno + 1
                    if func_length > 50:
                        self.issues.append({
                            'type': 'quality',
                            'severity': 'medium',
                            'category': 'Function Too Long',
                            'line_number': node.lineno,
                            'title': f'Function "{node.name}" is too long ({func_length} lines)',
                            'description': f'Function "{node.name}" has {func_length} lines',
                            'impact': 'Long functions are harder to test, understand, and maintain',
                            'suggested_fix': 'Consider breaking this function into smaller, more focused functions'
                        })
                self.generic_visit(node)
        
        checker = FunctionLengthChecker(self.lines)
        checker.visit(tree)
        self.issues.extend(checker.issues)
    
    def _check_bare_except(self):
        """Check for bare except clauses"""
        for i, line in enumerate(self.lines, 1):
            if re.search(r'except\s*:', line):
                self.issues.append({
                    'type': 'quality',
                    'severity': 'medium',
                    'category': 'Bare Exception Handler',
                    'line_number': i,
                    'title': 'Bare except clause found',
                    'description': 'Using bare except catches all exceptions including SystemExit and KeyboardInterrupt',
                    'impact': 'Can hide bugs and make debugging difficult',
                    'suggested_fix': 'Specify the exception type: except Exception: or except SpecificException:'
                })
    
    def _check_dangerous_functions(self):
        """Check for potentially dangerous function calls"""
        dangerous_patterns = {
            r'eval\s*\(': ('eval()', 'Unsafe function', 'critical', 'Executing arbitrary code'),
            r'exec\s*\(': ('exec()', 'Unsafe function', 'critical', 'Executing arbitrary code'),
            r'__import__\s*\(': ('__import__()', 'Dynamic import', 'high', 'Dynamic imports can load malicious code'),
            r'pickle\.loads': ('pickle.loads()', 'Unsafe deserialization', 'critical', 'Can execute arbitrary code'),
            r'subprocess\.call\s*\(': ('subprocess.call()', 'Command injection risk', 'high', 'Shell command execution'),
        }
        
        for i, line in enumerate(self.lines, 1):
            for pattern, (func, category, severity, impact) in dangerous_patterns.items():
                if re.search(pattern, line):
                    self.issues.append({
                        'type': 'security',
                        'severity': severity,
                        'category': category,
                        'line_number': i,
                        'title': f'Dangerous function: {func}',
                        'description': f'Line contains {func}',
                        'impact': impact,
                        'suggested_fix': 'Use safer alternatives or ensure input is properly validated',
                        'cwe': 'CWE-95',
                        'cwe_url': 'https://cwe.mitre.org/data/definitions/95.html'
                    })
    
    def _check_division_by_zero(self, tree):
        """Check for potential division by zero"""
        class DivisionChecker(ast.NodeVisitor):
            def __init__(self):
                self.issues = []
            
            def visit_BinOp(self, node):
                if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                    if isinstance(node.right, ast.Constant) and node.right.value == 0:
                        self.issues.append({
                            'type': 'bug',
                            'severity': 'critical',
                            'category': 'Division by Zero',
                            'line_number': node.lineno,
                            'title': 'Division by zero',
                            'description': 'Code divides by zero',
                            'impact': 'Will raise ZeroDivisionError at runtime',
                            'suggested_fix': 'Check that the divisor is not zero before dividing'
                        })
                self.generic_visit(node)
        
        checker = DivisionChecker()
        checker.visit(tree)
        self.issues.extend(checker.issues)
    
    def _check_uninitialized_variables(self, tree):
        """Check for variables that may not be initialized in all code paths"""
        class UninitializedChecker(ast.NodeVisitor):
            def __init__(self):
                self.issues = []
                self.in_if = False
            
            def visit_If(self, node):
                self.in_if = True
                self.generic_visit(node)
                self.in_if = False
        
        checker = UninitializedChecker()
        checker.visit(tree)
        self.issues.extend(checker.issues)
    
    def _analyze_javascript(self):
        """JavaScript/TypeScript analysis using regex patterns"""
        for i, line in enumerate(self.lines, 1):
            # Check for console.log in production code
            if 'console.log' in line and 'test' not in self.code.lower():
                self.issues.append({
                    'type': 'quality',
                    'severity': 'low',
                    'category': 'Debug Code',
                    'line_number': i,
                    'title': 'console.log in production code',
                    'description': 'Found console.log statement',
                    'impact': 'Console statements should be removed before deployment',
                    'suggested_fix': 'Remove or use a logging library instead'
                })
            
            # Check for var keyword
            if re.search(r'\bvar\s+\w+', line):
                self.issues.append({
                    'type': 'quality',
                    'severity': 'medium',
                    'category': 'Legacy Variable Declaration',
                    'line_number': i,
                    'title': 'Using var instead of let/const',
                    'description': 'Variable declared with var instead of let or const',
                    'impact': 'var has confusing scoping rules and should be avoided',
                    'suggested_fix': 'Replace var with let or const'
                })
            
            # Check for == instead of ===
            if '==' in line and '===' not in line:
                self.issues.append({
                    'type': 'quality',
                    'severity': 'medium',
                    'category': 'Loose Equality',
                    'line_number': i,
                    'title': 'Using == instead of ===',
                    'description': 'Using loose equality operator',
                    'impact': 'Can lead to unexpected type coercion bugs',
                    'suggested_fix': 'Use === for strict equality comparison'
                })
    
    def _analyze_java(self):
        """Java-specific analysis"""
        for i, line in enumerate(self.lines, 1):
            # Check for synchronization issues
            if 'synchronized' not in self.code and 'Thread' in line:
                pass  # Would need more context
    
    def _analyze_generic(self):
        """Generic code analysis for unsupported languages"""
        for i, line in enumerate(self.lines, 1):
            # Check for hardcoded credentials
            if self._contains_hardcoded_secret(line):
                self.issues.append({
                    'type': 'security',
                    'severity': 'critical',
                    'category': 'Hardcoded Credential',
                    'line_number': i,
                    'title': 'Hardcoded secret found',
                    'description': 'Line appears to contain a hardcoded secret',
                    'impact': 'Exposed credentials can be exploited',
                    'suggested_fix': 'Use environment variables or secret management',
                    'cwe': 'CWE-798',
                    'cwe_url': 'https://cwe.mitre.org/data/definitions/798.html'
                })
    
    def _contains_hardcoded_secret(self, line: str) -> bool:
        """Check if line contains hardcoded secrets"""
        patterns = [
            r'password\s*[=:]\s*["\'][^\'"]+["\']',
            r'api[_-]?key\s*[=:]\s*["\'][^\'"]+["\']',
            r'secret\s*[=:]\s*["\'][^\'"]+["\']',
            r'token\s*[=:]\s*["\'][^\'"]+["\']',
        ]
        
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
