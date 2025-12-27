from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Author must have a name")

        existing_author = Author.query.filter_by(name=value).first()
        if existing_author:
            raise ValueError("Author name must be unique")

        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Phone number must be exactly ten digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250))
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    CLICKBAIT_WORDS = [
        "Won't Believe",
        "Secret",
        "Top",
        "Guess"
    ]

    # Validators
    @validates('title')
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Post must have a title")

        if not any(word in value for word in self.CLICKBAIT_WORDS):
            raise ValueError("Title must be clickbait-y")

        return value

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Content must be at least 250 characters")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary must be 250 characters or less")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
