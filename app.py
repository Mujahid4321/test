import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/check_env')
def check_env():
    # Fetch the value of the environment variable
    db_credentials = os.getenv('DB_CREDENTIALS')

    if db_credentials:
        return jsonify({'message': 'Environment variable is set'})
    else:
        return jsonify({'error': 'Environment variable is not set'}), 500

if __name__ == '__main__':
    app.run(debug=True)
