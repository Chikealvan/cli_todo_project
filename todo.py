# import click
# from sqlalchemy import create_engine, Column, Integer, String. ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Create a SQLite database and establish a connection
# engine = create_engine('sqlite:///todo.db')
# Base = declarative_base()

# class Task(Base):
#     __tablename__ = 'tasks'

#     id = Column(Integer, primary_key=True)
#     task = Column(String)

# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)

# @click.group()
# @click.pass_context
# def todo(ctx):
#     """CLI Todo Project"""
#     ctx.ensure_object(dict)
#     ctx.obj["session"] = Session()

# @todo.command()
# @click.pass_context
# def tasks(ctx):
#     """Display tasks"""
#     session = ctx.obj["session"]
#     tasks = session.query(Task).all()

#     if tasks:
#         click.echo('YOUR TASKS\n**********')
#         for task in tasks:
#             click.echo(f"• {task.task} (ID: {task.id})")
#         click.echo('')
#     else:
#         click.echo("No tasks yet! Use ADD to add one.\n")

# @todo.command()
# @click.pass_context
# @click.option("-add", "--add_task", prompt="Enter task to add")
# def add(ctx, add_task):
#     """Add a task"""
#     if add_task:
#         session = ctx.obj["session"]
#         task = Task(task=add_task)
#         session.add(task)
#         session.commit()
#         click.echo(f"Added task '{add_task}' with ID {task.id}")

# @todo.command()
# @click.pass_context
# @click.option('-fin', '--fin_taskid', prompt='Enter ID of task to finish', type=int)
# def done(ctx, fin_taskid):
#     """Delete a task by ID"""
#     session = ctx.obj["session"]
#     task = session.query(Task).filter(Task.id == fin_taskid).first()

#     if task:
#         task_text = task.task
#         session.delete(task)
#         session.commit()
#         click.echo(f"Finished and removed task '{task_text}' with id {fin_taskid}")
#     else:
#         click.echo(f"Error: no task with id {fin_taskid}")

# if __name__ == "__main__":
#     todo()



import click
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create a SQLite database and establish a connection
engine = create_engine('sqlite:///todo.db')
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    labels = relationship('Label', secondary='task_labels')

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship('Task', back_populates='category')

class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship('Task', secondary='task_labels')

class TaskLabel(Base):
    __tablename__ = 'task_labels'

    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    label_id = Column(Integer, ForeignKey('labels.id'), primary_key=True)

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)

@click.group()
@click.pass_context
def todo(ctx):
    """CLI Todo Project"""
    ctx.ensure_object(dict)
    ctx.obj["session"] = Session()

@todo.command()
@click.pass_context
def tasks(ctx):
    """Display tasks"""
    session = ctx.obj["session"]
    tasks = session.query(Task).all()

    if tasks:
        click.echo('YOUR TASKS\n**********')
        for task in tasks:
            click.echo(f'• {task.task} (ID: {task.id}), Category: {task.category.name}, Labels: {", ".join(label.name for label in task.labels)}')
        click.echo('')
    else:
        click.echo("No tasks yet! Use ADD to add one.\n")

@todo.command()
@click.pass_context
@click.option("-add", "--add_task", prompt="Enter task to add")
@click.option("-category", "--category_name", prompt="Enter task category")
@click.option("-labels", "--label_names", prompt="Enter labels (comma-separated)")
def add(ctx, add_task, category_name, label_names):
    """Add a task"""
    session = ctx.obj["session"]

    # Check if the category already exists or create a new one
    category = session.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)

    # Split label_names and check if labels exist, creating new ones if needed
    label_names = [label.strip() for label in label_names.split(',')]
    labels = []
    for label_name in label_names:
        label = session.query(Label).filter(Label.name == label_name).first()
        if not label:
            label = Label(name=label_name)
        labels.append(label)

    task = Task(task=add_task, category=category, labels=labels)
    session.add(task)
    session.commit()
    click.echo(f"Added task '{add_task}' with ID {task.id}")

@todo.command()
@click.pass_context
@click.option('-fin', '--fin_taskid', prompt='Enter ID of task to finish', type=int)
def done(ctx, fin_taskid):
    """Delete a task by ID"""
    session = ctx.obj["session"]
    task = session.query(Task).filter(Task.id == fin_taskid).first()

    if task:
        task_text = task.task
        session.delete(task)
        session.commit()
        click.echo(f"Finished and removed task '{task_text}' with id {fin_taskid}")
    else:
        click.echo(f"Error: no task with id {fin_taskid}")

if __name__ == "__main__":
    todo()
