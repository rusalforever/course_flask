import requests
from flask import Flask, jsonify, request, Response, render_template

from models.pydantic.models import AnimalCreate, AnimalResponse
from typing import Union
from settings import settings
from database import init_db
from models.sqlalchemy.models import Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_uri

db = init_db(app)


def get_random_dog_photo():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    return data['message']


def get_random_cat_photo():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    return data[0]['url']


@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/animals', methods=['GET'])
def index() -> Response:
    animals = Animal.query.all()
    return jsonify({"animals": [AnimalResponse.model_validate(animal).model_dump(mode='json') for animal in animals]})


@app.route('/animal', methods=['POST'])
def add_animal() -> tuple[Response, int]:
    data = AnimalCreate(**request.get_json())

    if not data.photo_url:
        if data.animal_type.lower() == 'dog':
            photo_url = get_random_dog_photo()
        elif data.animal_type.lower() == 'cat':
            photo_url = get_random_cat_photo()
        else:
            photo_url = None
    else:
        photo_url = data.photo_url

    new_animal = Animal(
        animal_type=data.animal_type,
        name=data.name,
        birth_date=data.birth_date,
        breed=data.breed,
        photo_url=photo_url,
        animal_age=data.age
    )
    db.session.add(new_animal)
    db.session.commit()
    return jsonify(
        {
            "message": "Animal added successfully!",
            "animal": AnimalResponse.model_validate(new_animal).model_dump(mode='json')
        }
    ), 201


@app.route('/animal/<int:pk>', methods=['PUT'])
def update_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    data = AnimalCreate(**request.get_json())
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    animal.animal_type = data.animal_type
    animal.name = data.name
    animal.birth_date = data.birth_date
    animal.breed = data.breed

    if data.photo_url:
        animal.photo_url = data.photo_url

    db.session.commit()
    return jsonify(
        {
            "message": "Animal updated successfully!",
            "animal": AnimalResponse.model_validate(animal).model_dump(mode='json'),
        },
    )


@app.route('/animal/<int:pk>', methods=['GET'])
def retrieve_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    return jsonify(
        {
            "animal": AnimalResponse.model_validate(animal).model_dump(mode='json'),
        }
    )


@app.route('/animal/<int:pk>', methods=['DELETE'])
def delete_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deleted successfully!"})


@app.route('/health')
def health():
    return '', 200


def initialize_app():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)
