from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from rest_api import app
from the_foodie_network_app.database.models import db


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()