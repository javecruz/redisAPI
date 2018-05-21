from dbFlaskLink import db

class Fichero(db.Model):
    __tablename__ = 'ficheros'

    id = db.Column('id', db.Integer, primary_key = True)
    nombre = db.Column('nombre', db.VARCHAR)
    tipo = db.Column('tipo', db.VARCHAR)
    id_Vehiculo =  db.Column('id_Vehiculo', db.Integer)

    def __init__(self, nombre, tipo, id_Vehiculo):
        self.nombre = nombre
        self.tipo = tipo
        self.id_Vehiculo = id_Vehiculo

