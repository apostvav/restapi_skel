#!/usr/bin/env python3

import os
from restapi_skel import create_app, db
from restapi_skel.models import User, Task
from flask_migrate import Migrate
import click


app = create_app(os.getenv('RESTAPI_SKEL_ENV') or 'dev')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Task=Task)


@app.cli.command()
def insert_data():
    admin = User(username="admin", email="admin@example.com", password="admin")
    db.session.add(admin)
    task = Task(title='test', description='test description',
                date=None, due_date=None,
                done=False, user_id=1)
    db.session.add(task)
    db.session.commit()


@app.cli.command()
@click.confirmation_option(help='Are you sure you want to delete the db?')
def dropdb():
    db.drop_all()
    print("Database deleted")


@app.cli.command()
@click.confirmation_option(help="Are you sure you want to truncate db tables?")
def emptydb():
    for table in reversed(db.metadata.sorted_tables):
        print("Truncate table: "+str(table))
        db.engine.execute(table.delete())
    db.session.commit()
