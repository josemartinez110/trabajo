from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector, sqlite3



app = Flask(__name__)
app.secret_key = 'your_secret_key'



DATABASE = 'usuariosdb'

def init_db():
    conn = sqlite3.connect(DATABASE)
    with open('usuariosdb.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


@app.route('/')
def inicio():
    return render_template('index.html')

#--------------------------------------------------------USUARIOS-------------------------------------------------------------------------------


def insertar_usuario(nombre, apellido, edad):
    
    try:
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, edad) VALUES (%s, %s, %s)",
            (nombre, apellido, edad)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash("Error al insertar el usuario.")
    finally:
        if conn:
            conn.close()

def obtener_usuarios():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT nombre, apellido, edad FROM usuarios')
        usuarios = cursor.fetchall()
        return usuarios
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al obtener los usuarios.')
        return []
    finally:
        if conn:
            conn.close()


@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    edad = request.form['edad']

    if not nombre or not apellido or not edad:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, edad) VALUES (%s, %s, %s)",
            (nombre, apellido, edad)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash("Error al insertar el usuario.")
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

    return redirect(url_for('mostrar_usuarios'))


@app.route('/usuarios')
def mostrar_usuarios():
    usuarios = obtener_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)