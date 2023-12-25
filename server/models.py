from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

class Author(Base):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        assert name.strip(), "Author must have a name"
        existing_author = db.session.query(Author).filter(Author.name == name).first()
        assert not existing_author, "Author with this name already exists"
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        assert len(str(phone_number)) == 10, "Phone number must be exactly ten digits"
        return phone_number

class Post(Base):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        assert title.strip(), "Post must have a title"
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise AssertionError("Title must be sufficiently clickbait-y")
        return title

    @validates('content')
    def validate_content(self, key, content):
        assert len(content) >= 250, "Post content must be at least 250 characters long"
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        assert len(summary) <= 250, "Post summary must be a maximum of 250 characters"
        return summary

    @validates('category')
    def validate_category(self, key, category):
        assert category in ['Fiction', 'Non-Fiction'], "Invalid post category"
        return category
