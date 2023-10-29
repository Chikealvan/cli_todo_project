import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Configure logging for SQLAlchemy
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Create a SQLite database and establish a connection
engine = create_engine("sqlite:///todo_cli.db", echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)