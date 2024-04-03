from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, ARRAY, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os


app = Flask(__name__)

# Define your SQLAlchemy model for intents
Base = declarative_base()

class Intent(Base):
    __tablename__ = 'chatbot_data'
    __table_args__ = {'schema': 'chikkuchatbot'}
    id = Column(Integer, primary_key=True)
    tag = Column(String(50), unique=True, nullable=False)
    patterns = Column(ARRAY(String), nullable=False)
    responses = Column(ARRAY(String), nullable=False)

# Fetch the value of the DB_CREDENTIALS environment variable
db_credentials = os.getenv('DB_CREDENTIALS')

# Construct the database URL if credentials are provided
if db_credentials:
    db_user, db_password, db_host, db_port_str, db_name = db_credentials.split(';')
    db_port = int(db_port_str) if db_port_str and db_port_str.isdigit() else None
    db_url = f'postgresql://{db_user}:{quote_plus(db_password)}@{db_host}:{db_port}/{db_name}'


    # Create the SQLAlchemy engine and session outside the app context
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)

# API endpoint for adding new intents
@app.route('/api/intents', methods=['POST'])
def add_intent():
    data = request.get_json()

    tag = data.get('tag')
    patterns = data.get('patterns')
    responses = data.get('responses')

    # Validate data
    if not tag or not patterns or not responses:
        return jsonify({'error': 'Incomplete data provided'}), 400

    # Create a new intent
    new_intent = Intent(tag=tag, patterns=patterns, responses=responses)

    # Add the new intent to the database
    with app.app_context():
        session = Session()
        session.add(new_intent)
        session.commit()

    return jsonify({'message': 'Intent added successfully'})

# API endpoint for fetching all intents from the database
@app.route('/api/fetch', methods=['GET'])
def get_intents():
    # Create a session within the application context
    with app.app_context():
        session = Session()

        # Check if the 'Intent' table exists in the database
        inspector = inspect(engine)
        table_exists = inspector.has_table("chatbot_data", schema="chikkuchatbot")

        # Query data from the "chatbot_data" table if it exists
        if table_exists:
            intents = session.query(Intent).all()
            intent_list = []
            for intent in intents:
                intent_list.append({
                    'id': intent.id,
                    'tag': intent.tag,
                    'patterns': intent.patterns,
                    'responses': intent.responses
                })
        else:
            intent_list = []

    return jsonify({'intents': intent_list})

# API endpoint for getting the database URL
@app.route('/get_db_url')
def get_db_url():
    if db_credentials:
        return jsonify({'db_url': db_url})
    else:
        return jsonify({'error': 'DB_CREDENTIALS environment variable is not set'}), 500

if __name__ == '__main__':
    app.run(debug=True)
