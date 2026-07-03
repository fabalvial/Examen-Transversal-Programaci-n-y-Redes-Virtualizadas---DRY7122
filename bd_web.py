import sqlite3
import hashlib
from flask import Flask

app = Flask(__name__)
conn = sqlite3.connect('examen.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT, password TEXT)''')

# Usuarios actualizados con contraseñas a elección
usuarios = {
    "fabian alvial": "clave123", 
    "felipe armijo": "clave456",
    "nicolas farias": "clave789",
    "diego marchant": "clave000"
}

for user, pw in usuarios.items():
    hash_pw = hashlib.sha256(pw.encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios VALUES (?, ?)", (user, hash_pw))
conn.commit()

@app.route('/')
def home():
    return "Servidor activo en puerto 5800"

if __name__ == '__main__':
    app.run(port=5800)
