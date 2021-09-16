"# Microblog" 

# Włączanie:
set FLASK_APP = microblog.py

set FLASK_ENV = development

http://127.0.0.1:5000/


# Migracje

(venv)$ flask db migrate -m "what you did"

(venv)$ flask db upgrade
