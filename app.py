import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy for database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:muj321@localhost:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your Intent model using SQLAlchemy with the specified schema
class Intent(db.Model):
    __tablename__ = 'mujahd'
    __table_args__ = {'schema': 'chikkuchatbot'}
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True, nullable=False)
    patterns = db.Column(db.ARRAY(db.Text), nullable=False)
    responses = db.Column(db.ARRAY(db.Text), nullable=False)

# API endpoint for getting intents
@app.route('/api/intents', methods=['GET'])
def get_intents():
    with app.app_context():
        intents = Intent.query.all()
        intent_list = []
        for intent in intents:
            intent_list.append({
                'id': intent.id,
                'tag': intent.tag,
                'patterns': intent.patterns,
                'responses': intent.responses
            })

        return jsonify({'intents': intent_list})

if __name__ == '__main__':
    # Create database tables if not exists
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
