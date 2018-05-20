from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/empresa'
db = SQLAlchemy(app)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'

    id = db.Column('id', db.Integer, primary_key=True)
    matricula = db.Column('matricula', db.VARCHAR)
    fecha_fabricacion = db.Column('fecha_fabricacion', db.DateTime)
    marca = db.Column('marca', db.VARCHAR)
    modelo = db.Column('modelo', db.VARCHAR)
    id_cliente = db.Column('id_cliente', db.SMALLINT)
    tipo = db.Column('Tipo', db.SMALLINT)
