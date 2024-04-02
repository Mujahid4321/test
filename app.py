from flask import Flask
from sqlalchemy import create_engine
import os

app = Flask(__name__)

# Fetch database connection details from environment variables
db_host = os.getenv('DB_HOST')
db_port_str = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Check if required environment variables are set
if None in (db_host, db_port_str, db_name, db_user, db_password):
    raise ValueError("One or more required environment variables are not set.")

# Convert DB_PORT to integer if it's set and valid
db_port = int(db_port_str) if db_port_str.isdigit() else None

# Check if DB_PORT is None or not a valid integer
if db_port is None:
    raise ValueError("DB_PORT environment variable is not set or is not a valid integer.")

# Create a connection string
db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create an engine and connect to the database
engine = create_engine(db_url)

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
