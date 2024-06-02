from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, origin='*')

@app.route('/api/users', methods=['GET'])
def users():
    return jsonify({
        'users': [
            {'id': 1, 'name': 'John'},
            {'id': 2, 'name': 'Jane'}
    ]})


if __name__ == '__main__':
    app.run(debug=True, port=8080)