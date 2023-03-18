from flask import Flask, render_template, request, make_response, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import json

import forms

app=Flask(__name__)
app.config['SECRET_KEY'] = 'esta es una clave encriptada'
csrf = CSRFProtect(app)

@app.errorhandler(404)
def no_encontrada(e):
    return render_template("404.html")

@app.route("/cookies", methods=["GET", "POST"])
def cookies():
    reg_user = forms.LoginForm(request.form)

    if request.method == 'POST' and reg_user.validate():

        user = reg_user.username.data
        passw = reg_user.password.data
        datos = user + '@' + passw
        
        flash("Bienvenido {}".format(user))

        resp = make_response(render_template("cookies.html", form = reg_user))
        resp.set_cookie('username', user)
        resp.set_cookie('password', passw)
        resp.set_cookie('datos', datos)

        return resp
    
    return render_template("cookies.html", form = reg_user)

@app.route('/saludo')
def saludo():
    valor_cookie = request.cookies.get('username')
    nombre = valor_cookie.split('@')
    return render_template('saludo.html')

@app.route('/formulario2', methods=['GET'])
def formulario2():
    return render_template('formulario2.html')

@app.route('/alumnos', methods=['GET', 'POST'])
def alumno():
    alum_form = forms.UserForm(request.form)
    matricula = ''
    nombre = ''
   
    if request.method == 'POST':
        matricula = alum_form.matricula.data
        nombre = alum_form.nombre.data
    
    return render_template('alumnos.html', form = alum_form, matricula = matricula, nombre = nombre)

@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    if request.method == 'POST':
        num = int(request.form.get('num'))
        return render_template('inputs.html', num = num)
    return render_template('input.html')

@app.route('/calculo', methods=['POST'])
def calculo():
    inputs = [int(request.form.get(f'input{i}')) for i in range(int(request.form.get('num')))]
    max_num = max(inputs)
    min_num = min(inputs)
    avg_num = sum(inputs) / len(inputs)
    num_count = {}
    for num in inputs:
        if num in num_count:
            num_count[num] += 1
        else:
            num_count[num] = 1
    return render_template('calculo.html', max_num=max_num, min_num=min_num, avg_num=avg_num, num_count=num_count)

@app.route('/traductor', methods = ['GET', 'POST'])
def traductor():
    resultado = request.args.get('resultado', '')
    traductor_form = forms.TraductorForm(request.form)
    esp = ''
    eng = ''
    if request.method == 'POST':
        esp = traductor_form.esp.data
        eng = traductor_form.eng.data
        file = open('traduccion.txt', 'a')
        file.write(str(esp).lower() + ":" + str(eng).lower() + ';')
        file.close()
    return render_template('traductor.html', form = traductor_form, esp = esp, eng = eng, resultado = resultado)

@app.route('/traductor/busqueda', methods = ['POST'])
def busqueda():
    idioma = str(request.form.get('idioma'))
    palabra = str(request.form.get('palabra'))
    resultado = 'No se encontro una traducción'  # Establecer un valor predeterminado
    if idioma and palabra:
        with open('traduccion.txt', 'r') as file:
            query = {}
            with open('traduccion.txt', 'r') as file:
                lines = file.read().split(';')
                for line in lines:
                    if line.strip():
                        spanish, english = line.split(':')
                        query[spanish.strip()] = english.strip()
        if idioma == 'esp':
            resultado = query.get(palabra, 'No se encontro una traducción')
        elif idioma == 'eng':
            for key, value in query.items():
                if value == palabra:
                    resultado = key
                    break
    return redirect(url_for('traductor', resultado=resultado))

@app.route('/resistencias', methods = ['GET', 'POST'])
def resistencias():
    resistencias_forms = forms.ResistenciasForm(request.form)
    if request.method == 'GET':
        cookies = request.cookies.get('resistencia')
        if cookies:
            datos = json.loads(cookies)
        else:
            datos = {
                'c1': { 'text':'n/a', 'color':'' },
                'c2': { 'text':'n/a', 'color':'' },
                'c3': { 'text':'n/a', 'color':'' },
                'c4': { 'text':'n/a', 'color':'' },
                'val': { 'text':'n/a', 'color':'' },
                'min': { 'text':'n/a', 'color':'' },
                'max': { 'text':'n/a', 'color':'' },
            }
    elif request.method == 'POST':
        with open('colores.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        colors = {}
        for line in lines:
            parts = line.strip().split(';')
            color = {
                'color': parts[1],
                'banda1': int(parts[2]),
                'banda2': int(parts[3]),
                'multiplicador': float(parts[4]),
                'tolerancia': int(parts[5]),
            }
            colors[parts[0]] = color

        banda1 = str(request.form.get('banda1'))
        if banda1 in colors:
            b1 = colors[banda1]

        banda2 = str(request.form.get('banda2'))
        if banda2 in colors:
            b2 = colors[banda2]

        multiplicador = str(request.form.get('multiplicador'))
        if multiplicador in colors:
            m = colors[multiplicador]

        tolerancia = str(request.form.get('tolerancia'))
        if tolerancia in colors:
            t = colors[tolerancia]
        else:
            t = {
                'tolerancia': 20,
                'color': 'Sin Tolerancia',
            }
            tolerancia = 'sin'

        p1 = str(b1['banda1']) + str(b2['banda2'])

        val = int(p1) * m['multiplicador']
        mini = val - val / 100 * t['tolerancia']
        maxi = val + val / 100 * t['tolerancia']
        
        datos = {
            'c1': { 'text':b1['color'], 'clase': banda1 },
            'c2': { 'text':b2['color'], 'clase': banda2 },
            'c3': { 'text':m['color'], 'clase': multiplicador },
            'c4': { 'text':t['color'], 'clase': tolerancia },
            'val': { 'text':val, 'clase':'white' },
            'min': { 'text':mini, 'clase':'white' },
            'max': { 'text':maxi, 'clase':'white' },
        }
        resp = make_response(render_template('resistencias.html', resistencias_forms=resistencias_forms, datos=datos))
        resp.set_cookie('resistencia', json.dumps(datos))
    return render_template('resistencias.html', resistencias_forms=resistencias_forms, datos = datos)

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True,port=3000)
