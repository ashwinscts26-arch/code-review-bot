import json
import os
from typing import Dict, Any, Optional, List


class ClaudeReviewer:
    """Integrates Claude AI for intelligent code review"""
    
    def __init__(self, code: str, language: str, issues: List[Dict[str, Any]]):
        self.code = code
        self.language = language
        self.issues = issues
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
            except ImportError:
                self.client = None
    
    def review(self) -> Dict[str, Any]:
        """Get AI-powered review from Claude"""
        if not self.client or not self.api_key:
            return self._get_fallback_review()
        
        try:
            # Prepare the prompt
            prompt = self._build_prompt()
            
            # Call Claude API
            message = self.client.messages.create(
                model="claude-opus-4-6",  # or claude-sonnet-4-6
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse JSON response
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    review = json.loads(json_str)
                    return review
            except (json.JSONDecodeError, ValueError):
                # If JSON parsing fails, return fallback
                return self._get_fallback_review()
        
        except Exception as e:
            # If API call fails, return fallback
            print(f"Claude API error: {str(e)}")
            return self._get_fallback_review()
    
    def _build_prompt(self) -> str:
        """Build the prompt for Claude"""
        # Truncate code if too long
        code_to_review = self.code
        if len(code_to_review) > 5000:
            code_to_review = code_to_review[:5000] + "\n... (truncated)"
        
        issues_text = json.dumps(self.issues, indent=2)
        
        prompt = f"""You are an expert code reviewer. A code analysis tool has already performed static analysis on this {self.language} code and found the following issues:

{issues_text}

Here is the code:
```{self.language.lower()}
{code_to_review}
```

Please provide a comprehensive AI review in JSON format with the following structure:
{{
  "summary": "2-3 sentence overall assessment of the code quality and key concerns",
  "key_strengths": ["strength 1", "strength 2", ...],
  "main_concerns": ["concern 1", "concern 2", ...],
  "refactoring_suggestions": [
    {{
      "issue": "specific issue",
      "why": "explanation of why it matters",
      "refactored_code": "improved code snippet",
      "benefit": "what the refactoring improves"
    }},
    ...
  ],
  "best_practices": [
    {{
      "practice": "best practice name",
      "current_approach": "how it's currently done",
      "recommended_approach": "how it should be done",
      "impact": "why this matters"
    }},
    ...
  ],
  "overall_assessment": "detailed paragraph assessment"
}}

Be specific, actionable, and focus on the most important issues first. Only include refactoring suggestions for the top 2-3 concerns. Ensure the response is valid JSON."""
        
        return prompt
    
    def _get_fallback_review(self) -> Dict[str, Any]:
        """Generate a review without Claude API"""
        review = {
            "summary": self._generate_summary(),
            "key_strengths": self._extract_strengths(),
            "main_concerns": self._extract_concerns(),
            "refactoring_suggestions": self._generate_refactoring_suggestions(),
            "best_practices": self._generate_best_practices(),
            "overall_assessment": self._generate_assessment(),
            "fallback": True  # Indicate this is a fallback review
        }
        return review
    
    def _generate_summary(self) -> str:
        """Generate summary from issues"""
        issue_count = len(self.issues)
        critical_count = len([i for i in self.issues if i['severity'] == 'critical'])
        security_count = len([i for i in self.issues if i['type'] == 'security'])
        
        if critical_count > 0:
            summary = f"Critical issues detected: {critical_count} critical, {issue_count} total. Security and reliability review recommended."
        elif issue_count > 5:
            summary = f"Code has multiple issues ({issue_count}) affecting quality, security, and maintainability. Refactoring recommended."
        elif issue_count > 0:
            summary = f"Code has {issue_count} issue(s) that should be addressed. Generally acceptable with improvements needed."
        else:
            summary = "Code appears clean with no major issues detected. Well-structured and secure."
        
        return summary
    
    def _extract_strengths(self) -> List[str]:
        """Extract code strengths"""
        strengths = []
        
        # Check for absence of critical issues
        if len([i for i in self.issues if i['type'] == 'security']) == 0:
            strengths.append("No obvious security vulnerabilities detected")
        
        if len([i for i in self.issues if i['type'] == 'bug']) == 0:
            strengths.append("No obvious logic bugs or undefined variables")
        
        # Check code characteristics
        lines = self.code.split('\n')
        if all(len(line) < 100 for line in lines if line.strip()):
            strengths.append("Good line length keeping code readable")
        
        if len(lines) < 200:
            strengths.append("Compact code - easy to understand at a glance")
        
        if strengths:
            return strengths
        else:
            return ["Code follows basic structure"]
    
    def _extract_concerns(self) -> List[str]:
        """Extract main concerns from issues"""
        concerns = []
        
        # Group by severity and type
        security_issues = [i for i in self.issues if i['type'] == 'security']
        bug_issues = [i for i in self.issues if i['type'] == 'bug']
        quality_issues = [i for i in self.issues if i['type'] == 'quality']
        
        if security_issues:
            critical = len([i for i in security_issues if i['severity'] == 'critical'])
            concerns.append(f"Security: {critical} critical and {len(security_issues) - critical} high-priority issues")
        
        if bug_issues:
            critical = len([i for i in bug_issues if i['severity'] == 'critical'])
            concerns.append(f"Reliability: {critical} potential bugs that could crash the code")
        
        if quality_issues:
            concerns.append(f"Code Quality: {len(quality_issues)} maintainability and style issues")
        
        return concerns if concerns else ["Minor code style issues"]
    
    def _generate_refactoring_suggestions(self) -> List[Dict[str, str]]:
        """Generate refactoring suggestions for top issues"""
        suggestions = []
        
        # Find top issues
        critical_issues = [i for i in self.issues if i['severity'] == 'critical'][:2]
        high_issues = [i for i in self.issues if i['severity'] == 'high'][:2]
        top_issues = critical_issues + high_issues
        
        for issue in top_issues[:3]:  # Max 3 suggestions
            suggestion = {
                "issue": issue.get('title', 'Code Issue'),
                "why": issue.get('description', ''),
                "refactored_code": issue.get('suggested_fix', 'Apply the recommended fix'),
                "benefit": issue.get('impact', '')
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_best_practices(self) -> List[Dict[str, str]]:
        """Generate best practice recommendations"""
        practices = []
        
        # Language-specific practices
        if self.language.lower() == 'python':
            practices.append({
                "practice": "Exception Handling",
                "current_approach": "Using bare except or generic exceptions",
                "recommended_approach": "Catch specific exception types",
                "impact": "Makes debugging easier and prevents masking critical errors"
            })
        
        elif self.language.lower() in ['javascript', 'typescript']:
            practices.append({
                "practice": "Variable Declarations",
                "current_approach": "Using var keyword",
                "recommended_approach": "Use let and const with block scoping",
                "impact": "Prevents hoisting bugs and provides better scoping"
            })
        
        practices.append({
            "practice": "Code Comments",
            "current_approach": "Self-documenting code only",
            "recommended_approach": "Add docstrings/comments for complex logic",
            "impact": "Makes code maintenance easier for future developers"
        })
        
        return practices
    
    def _generate_assessment(self) -> str:
        """Generate detailed assessment"""
        issue_count = len(self.issues)
        
        if issue_count == 0:
            assessment = "This code is clean and well-structured with no detected issues. It demonstrates good practices and is ready for production use with standard testing and deployment procedures."
        elif issue_count < 5:
            assessment = f"This code has {issue_count} minor to moderate issue(s). With the suggested fixes applied, it would be production-ready. Focus on addressing the most critical issues first."
        elif issue_count < 10:
            assessment = f"This code has {issue_count} issues that need attention. Review and address the critical security and reliability issues before deployment. The codebase has potential but needs refactoring."
        else:
            assessment = f"This code has {issue_count} issues and needs significant review. Multiple security vulnerabilities and bugs are present. Consider a comprehensive code review and refactoring before deployment."
        
        return assessment
