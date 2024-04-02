import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Fetch database connection details from environment variable
db_credentials = os.getenv('DB_CREDENTIALS')

if db_credentials:
    # Split the credentials into individual components
    db_user, db_password, db_host, db_port, db_name = db_credentials.split(';')

    # Validate that db_port is a valid integer
    try:
        db_port = int(db_port)
    except ValueError:
        raise ValueError("DB_PORT in DB_CREDENTIALS is not a valid integer.")

    # Construct the database URL
    db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Create the database engine
    engine = create_engine(db_url)

    # Create a session factory
    Session = sessionmaker(bind=engine)

else:
    raise ValueError("DB_CREDENTIALS environment variable is not set.")


# Route to demonstrate accessing the database within Flask
@app.route('/')
def index():
    # Create a session using the session factory
    session = Session()

    try:
        # Perform database operations using 'session' within the Flask route
        # For example:
        # result = session.execute("SELECT * FROM my_table")
        # for row in result:
        #     print(row)
        return 'Hello, World!'
    finally:
        # Close the session to release resources
        session.close()


if __name__ == '__main__':
    app.run(debug=True)
