from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

#conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'abaco'

conexion = MySQL(app)

@app.before_request
def before_request():
    print("Antes de la peticion ...")

@app.after_request
def after_request(responder):
    print("Despues de la peticion")
    return responder

@app.route("/")
def index():
    #return "<h1>Hola mundo - sucribete</h1>"
    cursos = ['php', 'python', 'java', 'javascript', 'kotlin', 'dart']
    data = {
        'titulo': 'index123',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "OK" 

@app.route('/cursor')
def listar_cursor():
    data={}
    try:
        cursor=conexion.connction.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        cursor=cursor.fetchall()
        #print(cursor)
        data['cursor']=cursor
        data['mensaje']='Exito'
    except Exception as ex:
        data['mensaje']='Error ...'
    return jsonify(data)

def pagina_no_encontrada(error):
    #return render_template('404.html'), 404
    return redirect(url_for('index'))


if __name__ =='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)