from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# creates a table posts1 in the DB
# sqlalchemy will only look for table name in the Db if no table exists with that name a New table will be created.
# if a table with that name exists it wont touch that table again and changes made to table will not reflect


class Post(Base):
    __tablename__ = "posts1"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    number = Column(String, server_default="1234567890", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
