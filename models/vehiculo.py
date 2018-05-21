from .dbFlaskLink import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'

    id = db.Column('id', db.Integer, primary_key = True)
    matricula = db.Column('matricula', db.VARCHAR)
    fecha_fabricacion = db.Column('fecha_fabricacion', db.DateTime)
    marca = db.Column('marca', db.VARCHAR)
    modelo = db.Column('modelo', db.VARCHAR)
    id_cliente = db.Column('id_cliente', db.SMALLINT)
    Tipo = db.Column('Tipo', db.SMALLINT)

    def __init__(self, matricula, fecha, marca, modelo, id_cliente, tipo):
        self.matricula = matricula
        self.fecha_fabricacion = fecha
        self.marca = marca
        self.modelo = modelo
        self.id_cliente = id_cliente
        self.Tipo = tipo

