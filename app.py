import os
from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)

# Fetch database connection details from environment variable
db_credentials = os.getenv('DB_CREDENTIALS')
if db_credentials:
    db_user, db_password, db_host, db_port, db_name = db_credentials.split(';')
    db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(db_url)
else:
    raise ValueError("DB_CREDENTIALS environment variable is not set.")

@app.route('/')
def test_db_connection():
    try:
        # Perform a simple query to test the connection
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return f"Connection to PostgreSQL database successful: {result.scalar()}"

    except Exception as e:
        return f"Error connecting to database: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
