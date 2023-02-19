from flask import Flask, render_template, request

import forms

app=Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True,port=3000)
