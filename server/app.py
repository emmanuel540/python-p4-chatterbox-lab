
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_serialized = [message.to_dict() for message in messages]

        response = jsonify(messages_serialized)
        response.status_code = 200

        return response
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get("body"),
            username=data.get("username"),
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = jsonify(message_dict)
        response.status_code = 201

        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'GET':
        message_serialized = message.to_dict()

        response = jsonify(message_serialized)
        response.status_code = 200

        return response
   
    elif request.method == 'PATCH':
        message.body = request.get_json().get("body")

        db.session.commit()

        message_dict = message.to_dict()

        response = jsonify(message_dict)
        response.status_code = 200

        return response
   
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."    
        }

        response = jsonify(response_body)
        response.status_code = 200

        return response

if __name__ == '__main':
    app.run(port=5555)