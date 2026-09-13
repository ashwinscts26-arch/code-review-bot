#!/usr/bin/env python
"""
Sample vulnerable code for testing Code Review Bot analysis
Contains intentional security and code quality issues
"""

import os
import pickle
from flask import Flask, request

# Hardcoded credentials (Security Issue)
DATABASE_PASSWORD = "admin123secret"
API_KEY = "sk-1234567890abcdefghijklmnop"

app = Flask(__name__)


def unsafe_query(user_id):
    """SQL Injection vulnerability (CWE-89)"""
    query = "SELECT * FROM users WHERE id = " + user_id
    # This should use parameterized queries instead
    return query


def execute_command(filename):
    """Command Injection vulnerability (CWE-78)"""
    cmd = "cat " + filename  # Unsafe concatenation
    os.system(cmd)


def unsafe_deserialization(data):
    """Insecure deserialization (CWE-502)"""
    obj = pickle.loads(data)  # Dangerous with untrusted data
    return obj


def divide(a, b):
    """Division by zero risk (CWE-369)"""
    if b == 0:
        return None
    return a / b


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """XSS vulnerability (CWE-79)"""
    # User input directly rendered to HTML without escaping
    return f"<h1>User: {user_id}</h1>"


def long_function_that_does_too_much():
    """Code Quality Issue: Function too long"""
    x = 1
    y = 2
    z = x + y
    print(z)
    
    result = []
    for i in range(100):
        result.append(i * 2)
    
    data = []
    for item in result:
        if item % 2 == 0:
            data.append(item)
    
    # More than 50 lines of code in a single function
    # This should be broken into smaller, more testable functions
    
    output = ""
    for d in data:
        output += str(d) + ","
    
    try:
        val = output.split(",")
        return val
    except:  # Bare except (CWE-251)
        print("Error occurred")


def weak_crypto():
    """Weak cryptography (CWE-326)"""
    import hashlib
    password = "secret123"
    
    # MD5 is cryptographically broken
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed


def eval_danger(code):
    """Dangerous eval usage (CWE-95)"""
    result = eval(code)  # Never do this with untrusted input!
    return result


# Variable that may not be initialized in all paths
def check_status(status):
    """Undefined variable issue"""
    if status == "active":
        user_count = 10
    elif status == "inactive":
        user_count = 0
    
    # user_count may not be defined if status is neither "active" nor "inactive"
    return user_count


if __name__ == "__main__":
    # Using var comparison in Python is less of an issue,
    # but loose equality is a concern in JavaScript/PHP
    app.run(debug=True)
