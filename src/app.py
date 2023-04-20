"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "id": jackson_family._generateId(),
    "first_name": "John",
    "last_name": "Jackson",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "id": jackson_family._generateId(),
    "first_name": "Jane",
    "last_name": "Jackson",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "id": jackson_family._generateId(),
    "first_name": "Jimmy",
    "last_name": "Jackson",
    "age": 5,
    "lucky_numbers": [1]
})
jackson_family.add_member({
    "id": jackson_family._generateId(),
    "first_name": "Felipe",
    "last_name": "Jackson",
    "age": 29,
    "lucky_numbers": [1, 8, 12, 16]
})



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def handle_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if member is None:
        raise APIException("Member not found", status_code=404)

    response_body = {
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }

    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def handle_new_member():

    # this is how you can use the Family datastructure by calling its methods
    request_body = request.get_json()
    if request_body is None:
        raise APIException("Request body must be JSON", status_code=400)

    member = {
        "id": jackson_family._generateId(),
        "first_name": request_body.get("first_name", ""),
        "last_name": "Jackson",
        "age": request_body.get("age", 0),
        "lucky_numbers": request_body.get("lucky_numbers", [])
    }
    jackson_family.add_member(member)

    response_body = {
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['PUT'])
def handle_update_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    request_body = request.get_json()
    if request_body is None:
        raise APIException("Request body must be JSON", status_code=400)

    member = {
        "id": member_id,
        "first_name": request_body.get("first_name", ""),
        "last_name": request_body.get("last_name", ""),
        "age": request_body.get("age", ""),
        "lucky_numbers": request_body.get("lucky_numbers", [])
        }
    Family.update_member(member_id, member)
    return jsonify({"msg": "Member updated successfully"}), 200


@app.route('/member/int:member_id', methods=['DELETE'])
def handle_delete_member(member_id):
    Family.delete_member(member_id)
    return jsonify({"msg": "Member deleted successfully"}), 200

@app.errorhandler(APIException)
def handle_api_exception(error):
    return jsonify({"msg": error.message}), error.status_code

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
