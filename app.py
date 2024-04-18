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


def get_dog_image():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    if response.status_code == 200:
        return response.json()['message']
    return None


def get_cat_image():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    if response.status_code == 200:
        return response.json()[0]['url']
    return None

def get_photo_url(animal_type):
    photo_functions = {
        'dog': get_dog_image,
        'cat': get_cat_image
    }
    get_photo = photo_functions.get(animal_type.lower())
    return get_photo() if get_photo else None



@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/health')
def health() -> tuple[str, int]:
    return "", 200


@app.route('/animals', methods=['GET'])
def index() -> Response:
    animals = Animal.query.all()
    return jsonify({"animals": [AnimalResponse.model_validate(animal).model_dump(mode='json') for animal in animals]})


@app.route('/animal', methods=['POST'])
def add_animal() -> tuple[Response, int]:
    data = AnimalCreate(**request.get_json())
    if not data.photo_url:
        data.photo_url = get_photo_url(data.animal_type)
    new_animal = Animal(
        animal_type=data.animal_type,
        name=data.name,
        birth_date=data.birth_date,
        breed=data.breed,
        photo_url=data.photo_url,
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

    if not data.photo_url:
        data.photo_url = get_photo_url(data.animal_type)
    animal.animal_type = data.animal_type
    animal.name = data.name
    animal.birth_date = data.birth_date
    animal.breed = data.breed
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


def initialize_app():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)
