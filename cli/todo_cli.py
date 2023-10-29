import click
from sqlalchemy.orm import sessionmaker
from models.database import Base, engine
from models.task_model import Category, Task, Label  # Import the models

Session = sessionmaker(bind=engine)

@click.group()
@click.pass_context
def todo(ctx):
    """CLI Todo Project"""
    ctx.ensure_object(dict)
    ctx.obj["session"] = Session()

    # import pdb; pdb.set_trace()  # Add this line for debugging

@todo.command()
def dbinit():
    """Initialize the database."""
    Base.metadata.create_all(engine)

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

    category = session.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)

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