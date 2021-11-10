from web_app import db


# Define object that will be stored in DB
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # printable version of the object
    def __repr__(self):
        return f'{self.title} created on: {self.date}'


class CrewMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # name of crew member
    is_skipper = db.Column(db.Boolean, nullable=False, default=True)  # flags skipper
    crew_id = db.Column(db.Integer, nullable=False)  # ID of crew to which crew member belong

    # printable version of the object
    def __repr__(self):
        return f'Crew member: {self.name} - {"Skipper" if self.is_skipper else ""} - member of crew: {self.crew_id}'


class Crew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.Integer, nullable=False)  # ID of crew to which crew members belong
    # Ref: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    watch_duration = db.Column(db.Integer, nullable=False)

    # printable version of the object
    def __repr__(self):
        return f'Crew #: {self.crew_id} - from {self.start_date.strftime("%m/%d/%Y-%H:%M")} to ' \
               f'{self.end_date.strftime("%m/%d/%Y-%H:%M")} - Watch duration: {self.watch_duration}'

# FYI: this is important
# Fixes this error: sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table
# Instantiate DB once we have defined objects - needs to be after Task and other DB entities
db.create_all()
