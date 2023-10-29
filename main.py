from sqlalchemy.orm import sessionmaker
from models.database import engine
from cli.todo_cli import todo

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    todo()
