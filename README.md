# Password-Manager
A secure password generator and encrypted storage tool.
# Password Generator & Manager

## Features

- Generate secure random passwords
- Customizable password length and character types
- Password strength checker with feedback
- Encrypted password storage (using Fernet encryption)
- Retrieve, list, and delete stored passwords

## Installation

```bash
pip install cryptography
```

## Usage

```bash
# Generate a secure password (default 16 characters)
python password_manager.py generate

# Generate a longer password
python password_manager.py generate --length 24

# Check password strength
python password_manager.py strength "MyP@ssw0rd123"

# Save a password entry
python password_manager.py save github myusername MyP@ss123

# Retrieve a stored password
python password_manager.py get github

# List all stored sites
python password_manager.py list

# Delete a password entry
python password_manager.py delete github

# Show help
python password_manager.py help
```

## Security Notes

- Passwords are encrypted using Fernet symmetric encryption
- The encryption key is stored in `.key` file (keep this safe!)
- Generated passwords use cryptographically secure random generation
- Never commit `.key` or `passwords.enc` to version control

## Files

- `password_manager.py` - Main application
- `.key` - Encryption key (auto-generated)
- `passwords.enc` - Encrypted password storage
