from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), unique=True, nullable=False)
    is_done = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
            return '<Todo %r>' % self.username
    
    def serialize(self):
            return {
                "id": self.id,
                "task": self.task,
                "is_done": self.is_done
                # do not serialize the password, its a security breach
            }
