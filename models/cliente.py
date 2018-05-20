from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/empresa'
db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column('id', db.SMALLINT, primary_key=True)
    nombres = db.Column('nombres', db.VARCHAR)
    ciudad = db.Column('ciudad', db.VARCHAR)
    sexo = db.Column('sexo', db.CHAR)
    telefono = db.Column('telefono', db.VARCHAR)
    fecha_nacimiento = db.Column('fecha_nacimiento', db.DateTime)
    direccion = db.Column('direccion', db.VARCHAR)
    provincia = db.Column('provincia', db.VARCHAR)
    fechaAlta = db.Column('fechaAlta', db.DateTime)




