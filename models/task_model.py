from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the database engine and create tables
engine = create_engine("sqlite:///todo_cli.db")

Base = declarative_base()

# Define the Task-Category relationship table
task_category_association = Table(
    "task_category_association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)

# Define the models
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="tasks")
    labels = relationship("Label", secondary="task_label_association")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship("Task", back_populates="category")

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship("Task", secondary="task_label_association")

task_label_association = Table(
    "task_label_association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Sample data for categories
categories_data = ["Work", "Personal", "Shopping"]

# Sample data for labels
labels_data = ["Urgent", "Important", "Home"]

# Sample data for tasks
tasks_data = [
    {"task": "Finish project presentation", "category_id": 1},
    {"task": "Buy groceries", "category_id": 3},
    {"task": "Call mom", "category_id": 2},
]

# Sample data for task-label relationships
task_labels_data = [(1, 2), (1, 3), (2, 1)]

# Insert sample data into the categories table
for category_name in categories_data:
    category = Category(name=category_name)
    session.add(category)

# Insert sample data into the labels table
for label_name in labels_data:
    label = Label(name=label_name)
    session.add(label)

# Insert sample data into the tasks table
for task_info in tasks_data:
    task = Task(**task_info)
    session.add(task)

# Insert sample data into the task-label relationships
for task_id, label_id in task_labels_data:
    task = session.query(Task).filter(Task.id == task_id).first()
    label = session.query(Label).filter(Label.id == label_id).first()
    task.labels.append(label)

# Commit the changes to the database
session.commit()

# Close the session when done
session.close()
