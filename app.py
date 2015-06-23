#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

 
app = Flask(__name__)

blog = [
    {
        'id': 1,
        'title': u'Day One',
        'entry': u'Hello this is day one', 
    },
    {
        'id': 2,
        'title': u'Learning Python',
        'description': u'Just trying to learn Python'
    }
]


def make_public_entry(entry):
    new_entry = {}
    for field in entry:
        if field == 'id':
            new_entry['uri'] = url_for('get_entry', entry_id=entry['id'], _external=True)
            new_entry['id'] = entry['id']
        else:
            new_entry[field] = entry[field]
    return new_entry

@app.route('/blog/api/v1.0/entries', methods=['GET'])
def get_entries():
    return jsonify({'entries': [make_public_entry(entry) for entry in blog]})


@app.route('/blog/api/v1.0/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    entry = [entry for entry in blog if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': entry[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
