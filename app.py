import os

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
    
    # Use db_url to create the database engine or connection
else:
    raise ValueError("DB_CREDENTIALS environment variable is not set.")
