from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading
import random as rd
import firebase_admin
from firebase_admin import credentials, firestore
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
socketio = SocketIO(app)

cred = credentials.Certificate("data-streaming-39988-firebase-adminsdk-54sqr-dac41d3dd2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



def data_generator():
    """Generador de datos simulados."""
    counter_1 = 0
    counter_2 = 0
    while True:
        time.sleep(0.5)  # Simular una nueva actualización cada segundo
        #counter += 1
        counter_1=counter_1+1
        counter_2=counter_2+2
        counter_3=rd.randint(1,100)
        counter_4=[counter_1,counter_2,counter_3]

        # Guarda los datos en Cloud Firestore
        doc_ref = db.collection('data').add({
            'contador_!': counter_1,
            'contador_2': counter_2,
            'contador_3': counter_3,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        yield counter_4

@app.route('/')
def index():
    """Renderiza la página de inicio."""
    return render_template('index.html')

def background_thread():
    """Envía datos continuos a través de WebSocket."""
    data_gen = data_generator()
    while True:
        socketio.emit('data', next(data_gen))
        socketio.sleep(1)  # Emitir datos cada segundo

@socketio.on('connect')
def handle_connect():
    """Maneja la conexión de un cliente WebSocket."""
    print('Cliente conectado')
    if not thread.is_alive():
        thread.start()

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    app.config['SECRET_KEY'] = 'secret!'
    socketio.run(app, debug=True)
