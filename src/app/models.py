from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.config import settings
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    )
#ALEMBIC command
# After changing models
# alembic revision --autogenerate -m "what you've changed"" 
# alembic upgrade head
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number=Column(String,nullable=True)
    is_active=Column(Boolean,nullable=False,default=True)
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'),nullable=False )
    #with this relationship we can access the user who created the post
    owner=relationship("User")

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'),nullable=False, primary_key=True)
    post_id=Column(Integer, ForeignKey('posts.id',ondelete='CASCADE'),nullable=False, primary_key=True)