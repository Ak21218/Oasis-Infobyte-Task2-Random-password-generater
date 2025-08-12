🔑 Random Password Generator – Python (CLI Version)
A secure and customizable command-line password generator built in Python.
Supports flexible password length, optional uppercase letters, numbers, and special characters.

📌 Features
- Custom Length – Choose any password length.
- Optional Character Sets – Easily exclude uppercase, numbers, or special characters.
- Ensures Security – Always includes at least one character from each chosen set.
- CLI Support – Pass options directly via terminal.

🛠️ Tech Stack
- Python 3.x

Libraries:
- random – Random selection
- string – Predefined character sets
- argparse – Command-line argument parsing


▶️ Usage
Run in terminal:
`python password_generator.py`

Example Commands:
# Generate a 16-character password
python password_generator.py -l 16

# Generate a password without uppercase letters
python password_generator.py -u

# Generate a password without numbers and special characters
python password_generator.py -n -s

# Generate a 20-character password without special characters
python password_generator.py -l 20 -s

Example Output:
Generated Password: A5n!k9T@3pZxLqW8

📂 Project Structure
- random-password-generator/
- │── password_generator.py   # CLI Python script
- │── README.md               # Documentation
  
🚀 Future Improvements
- Add a GUI version using Tkinter or PyQt.
- Implement a password strength meter.
- Option to save passwords to a file.
