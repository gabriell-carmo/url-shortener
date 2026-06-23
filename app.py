from flask import Flask
from database import get_db, close_db, init_db

app = Flask(__name__)

app.teardown_appcontext(close_db)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)