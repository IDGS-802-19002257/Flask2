from wtforms import Form
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField
from flask_wtf import FlaskForm

from wtforms.fields import EmailField, TextAreaField, RadioField, PasswordField
from wtforms import validators

def mi_Validacion(form, field):
    if len(field.data) == 0:
        raise validators.ValidationError('El campo no tiene datos')

class UserForm(Form):
    matricula = StringField('Matricula', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='long de campo 4 min and 5 max')
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido')
    ])
    apaterno = StringField('Apaterno', [mi_Validacion])
    amaterno = StringField('Amaterno')
    email = EmailField('Email')

class TraductorForm(Form):
    esp = StringField('Español', [
        validators.DataRequired(message='Este campo es requerido')
    ])
    eng = StringField('Inglés', [
        validators.DataRequired(message='Este campo es requerido')
    ])

class LoginForm(Form):
    username = StringField('usuario', [
        validators.DataRequired(message='El usuario es requerido')
    ])

    password = PasswordField('password', [
        validators.DataRequired(message='El usuario es requerido'),
        validators.length(min=4, max=10, message='long de campo 4 min and 5 max')
    ])

class ResistenciasForm(Form):
    banda1 = SelectField('Banda 1', choices=[
        ('black', 'Negro'),
        ('brown', 'Marrón'),
        ('red', 'Rojo'),
        ('orange', 'Naranja'),
        ('yellow', 'Amarillo'),
        ('green', 'Verde'),
        ('blue', 'Azul'),
        ('purple', 'Violeta'),
        ('gray', 'Gris'),
    ])
    banda2 = SelectField('Banda 2', choices=[
        ('black', 'Negro'),
        ('brown', 'Marrón'),
        ('red', 'Rojo'),
        ('orange', 'Naranja'),
        ('yellow', 'Amarillo'),
        ('green', 'Verde'),
        ('blue', 'Azul'),
        ('purple', 'Violeta'),
        ('gray', 'Gris'),
    ])
    multiplicador = SelectField('Multiplicador', choices=[
        ('black', 'Negro'),
        ('brown', 'Marrón'),
        ('red', 'Rojo'),
        ('orange', 'Naranja'),
        ('yellow', 'Amarillo'),
        ('green', 'Verde'),
        ('blue', 'Azul'),
        ('purple', 'Violeta'),
        ('gray', 'Gris'),
        ('gold', 'Dorado'),
        ('silver', 'Plateado')
    ])
    tolerancia = SelectField('Multiplicador', choices=[
        ('brown', 'Marrón'),
        ('red', 'Rojo'),
        ('gold', 'Dorado'),
        ('silver', 'Plateado'),
        ('na', 'Sin banda')
    ])
