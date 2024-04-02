import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_db_url')
def get_db_url():
    # Fetch the value of the DB_CREDENTIALS environment variable
    db_credentials = os.getenv('DB_CREDENTIALS')

    if db_credentials:
        # Split the credentials into individual components
        db_user, db_password, db_host, db_port, db_name = db_credentials.split(';')

        # Validate that db_port is a valid integer
        try:
            db_port = int(db_port)
        except ValueError:
            return jsonify({'error': 'DB_PORT in DB_CREDENTIALS is not a valid integer'}), 500

        # Construct the database URL
        db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

        return jsonify({'db_url': db_url})
    else:
        return jsonify({'error': 'DB_CREDENTIALS environment variable is not set'}), 500

if __name__ == '__main__':
    app.run(debug=True)
