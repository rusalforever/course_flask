from database import db


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    breed = db.Column(db.String, nullable=False)
    foto = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
