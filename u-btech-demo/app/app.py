import json
from flask import Flask, request, jsonify


# Returns book job ID
def get_bookjob(id: int) -> dict:
    return bookjobs.get(str(id))


# Checking if the book job ID is valid
def jobId_is_valid(bookjob: dict) -> bool:
    if not bookjob.get("name"):
        return False
    if not len(bookjob) == 1:
        return False
    return True


# json module in Python module provides a method called dump()
# which converts the Python objects into appropriate json objects.
# The dump() method is used when the Python objects have to be stored in a file.
# The dump() needs the json file name in which the output has to be stored as an argument.
# This method writes in the memory and then command for writing to disk is executed separately.
def write_json():
    with open("data.json", "w") as f:
        json.dump(bookjobs, f, indent=4)


# Find the max ID value, increment it by 1 and return the new ID
def get_new_key() -> str:
    return str(max(int(key) for key in bookjobs) + 1)


app = Flask(__name__)


@app.route('/bookjobs', methods=['GET'])
def get_bookjobs():
    return jsonify(bookjobs)


# to get a specific book job id add the ID value to the url
@app.route('/bookjobs/<int:id>', methods=['GET'])
def get_bookJob_by_id(id: int):
    bookjob = get_bookjob(id)
    if not bookjob:
        return jsonify({'error': 'Bookjob does not exist'}), 404
    return jsonify(bookjob)


@app.route('/bookjobs', methods=['POST'])
def create_bookjob():
    bookjob = json.loads(request.data)
    if not jobId_is_valid(bookjob):
        return jsonify({'error': 'Invalid bookjob properties.'}), 400
    new_key = get_new_key()
    bookjobs[new_key] = bookjob
    write_json()
    return '', 201, {'location': f'/bookjobs/{new_key}'}


@app.route('/bookjobs/<int:id>', methods=['DELETE'])
def delete_bookjob(id: int):
    bookjob = get_bookjob(id)
    if not bookjob:
        return jsonify({'error': 'Bookjob does not exist'}), 404
    del bookjobs[str(id)]
    write_json()
    return jsonify(bookjob), 200


with open("data.json") as f:
    bookjobs = json.load(f)


#app.run(host="0.0.0.0", port=5000)
