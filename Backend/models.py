from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class ToDo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)