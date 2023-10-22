from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages=Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.serialize() for message in messages])

@app.route('/messages', methods=['POST'])
def post_message():
    data=request.get_json()
    message=Message(body=data.get('body'),username=data.get('username'))
    db.session.add(message)
    db.session.commit()
    return jsonify(message.serialize()), 201
    

@app.route('/messages/<int:id>',methods=['PATCH'])
def messages_by_id(id):
    message = Message.query.get(id)
    if message is None:
        return jsonify({'error':'Message not found'}), 404
    
    data = request.get_json()
    message.body = data.get('body')
    db.session.commit()
    return jsonify(message.serialize())
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message is None:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'})


if __name__ == '__main__':
    app.run(port=5555)
