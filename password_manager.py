#!/usr/bin/env python3
"""
Password Generator & Manager
A secure password generator and storage tool with encryption.
"""

import json
import os
import secrets
import string
import hashlib
from cryptography.fernet import Fernet

DATA_FILE = "passwords.enc"
KEY_FILE = ".key"

def generate_key():
    """Generate or load encryption key."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def get_cipher():
    """Get Fernet cipher instance."""
    key = generate_key()
    return Fernet(key)

def generate_password(length=16, use_upper=True, use_lower=True, 
                      use_digits=True, use_symbols=True):
    """Generate a secure random password."""
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        print("Error: At least one character type must be selected")
        return None
    
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def check_password_strength(password):
    """Check password strength and return score."""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")
    
    if len(password) >= 12:
        score += 1
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    strength = {1: "Very Weak", 2: "Weak", 3: "Fair", 
                4: "Good", 5: "Strong", 6: "Very Strong"}
    
    return score, strength.get(score, "Unknown"), feedback

def save_password(site, username, password):
    """Save password entry to encrypted file."""
    cipher = get_cipher()
    
    data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'rb') as f:
                decrypted = cipher.decrypt(f.read())
                data = json.loads(decrypted)
        except:
            data = {}
    
    entry = {
        "site": site,
        "username": username,
        "password": password,
        "created_at": str(__import__('datetime').datetime.now())
    }
    
    data[site] = entry
    
    encrypted = cipher.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted)
    
    print(f"✓ Saved password for {site}")

def get_password(site):
    """Retrieve password for a site."""
    cipher = get_cipher()
    
    if not os.path.exists(DATA_FILE):
        print("No passwords stored yet")
        return None
    
    try:
        with open(DATA_FILE, 'rb') as f:
            decrypted = cipher.decrypt(f.read())
            data = json.loads(decrypted)
        
        if site in data:
            entry = data[site]
            print(f"\n{'='*40}")
            print(f"Site: {entry['site']}")
            print(f"Username: {entry['username']}")
            print(f"Password: {entry['password']}")
            print(f"Created: {entry['created_at']}")
            print(f"{'='*40}\n")
            return entry
        else:
            print(f"No entry found for {site}")
            return None
    except Exception as e:
        print(f"Error reading passwords: {e}")
        return None

def list_sites():
    """List all stored sites."""
    cipher = get_cipher()
    
    if not os.path.exists(DATA_FILE):
        print("No passwords stored yet")
        return
    
    try:
        with open(DATA_FILE, 'rb') as f:
            decrypted = cipher.decrypt(f.read())
            data = json.loads(decrypted)
        
        print("\n" + "="*40)
        print("STORED SITES")
        print("="*40)
        for i, site in enumerate(data.keys(), 1):
            print(f"{i}. {site}")
        print("="*40 + "\n")
    except Exception as e:
        print(f"Error reading passwords: {e}")

def delete_entry(site):
    """Delete a password entry."""
    cipher = get_cipher()
    
    if not os.path.exists(DATA_FILE):
        print("No passwords stored")
        return
    
    try:
        with open(DATA_FILE, 'rb') as f:
            decrypted = cipher.decrypt(f.read())
            data = json.loads(decrypted)
        
        if site in data:
            del data[site]
            encrypted = cipher.encrypt(json.dumps(data).encode())
            with open(DATA_FILE, 'wb') as f:
                f.write(encrypted)
            print(f"✓ Deleted entry for {site}")
        else:
            print(f"No entry found for {site}")
    except Exception as e:
        print(f"Error: {e}")

def show_help():
    """Display help information."""
    print("""
Password Manager Commands:
-------------------------
generate [--length N]                    Generate a secure password
strength <password>                      Check password strength
save <site> <username> <password>        Save a password entry
get <site>                               Retrieve password for site
list                                     List all stored sites
delete <site>                            Delete a password entry
help                                     Show this help message

Examples:
  python password_manager.py generate --length 20
  python password_manager.py strength "MyP@ssw0rd"
  python password_manager.py save github myuser MyP@ss123
  python password_manager.py get github
  python password_manager.py list
  python password_manager.py delete github
""")

def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "generate":
        length = 16
        if "--length" in sys.argv:
            idx = sys.argv.index("--length")
            if idx + 1 < len(sys.argv):
                try:
                    length = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        password = generate_password(length)
        if password:
            print(f"\nGenerated Password: {password}\n")
    
    elif command == "strength":
        if len(sys.argv) < 3:
            print("Usage: python password_manager.py strength \"your_password\"")
            return
        password = sys.argv[2]
        score, strength_name, feedback = check_password_strength(password)
        print(f"\nPassword Strength: {strength_name} ({score}/6)")
        if feedback:
            print("Suggestions:")
            for f in feedback:
                print(f"  - {f}")
        print()
    
    elif command == "save":
        if len(sys.argv) < 5:
            print("Usage: python password_manager.py save <site> <username> <password>")
            return
        site, username, password = sys.argv[2], sys.argv[3], sys.argv[4]
        save_password(site, username, password)
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python password_manager.py get <site>")
            return
        get_password(sys.argv[2])
    
    elif command == "list":
        list_sites()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python password_manager.py delete <site>")
            return
        delete_entry(sys.argv[2])
    
    elif command == "help":
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
