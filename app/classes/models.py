from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import app.db as db
class Feeds(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=False)

# class CheckResult(db.Model):
#     id = db.Column(db.Integer, primary_key=True)  
#     feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), index=True, nullable=False)  
#     picture_error_count = db.Column(db.Integer, nullable=False)  
#     name_error_count = db.Column(db.Integer, nullable=False)  
#     id_error_count = db.Column(db.Integer, nullable=False)  