# pip install flask-socketio

from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, send, emit

socketio = SocketIO()

@socketio.on('message')
def handle_message(message):
  send(message)

@socketio.on('json')
def handle_json(json):
  send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
  emit('my response', json)

def create_app():
  app = Flask(__name__)
  socketio.init_app(app)

  @app.get('/')
  def index():
    return "Cantina Fatec"

  return app

if __name__ == '__main__':
  app = create_app()
  socketio.run(app, allow_unsafe_werkzeug=True)
