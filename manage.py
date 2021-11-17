"""
manage: FLASK_APP
Reference: O'Reilly Flask Web Development
"""

import os
import click
from app import create_app, db
from app.models import User, Role, Animal, Association
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Animal=Animal, Association=Association)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
