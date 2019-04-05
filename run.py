from app import app
from db import db, init_db

db.init_app(app)


@app.before_first_request
def create_tables():
    print("Creating DB")
    db.create_all()
    print("Initializing DB")
    init_db()
