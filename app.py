from flask import Flask
from sqlalchemy import create_engine
import os  # Import the os module for accessing environment variables

app = Flask(__name__)

# Fetch database connection details from environment variables
db_host = os.getenv('DB_HOST')
db_port_str = os.getenv('DB_PORT')
db_port = int(db_port_str) if db_port_str and db_port_str.isdigit() else None
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

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
