# Emotion-Detection-App
Some instruction for downloading get the package is to working 
This is for vscode using macOS so it probably a little different for Windows

# First step in the terminal
pip3 install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator

# Second step in terminal
python3
from app import db
db.create_all()
exit()

#Third step in terminal
sqlite3 database.db
.tables
.exit
