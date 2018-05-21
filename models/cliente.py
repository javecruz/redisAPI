from .dbFlaskLink import db

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column('id', db.SMALLINT, primary_key=True)
    nombres = db.Column('nombres', db.VARCHAR)
    ciudad = db.Column('ciudad',db.VARCHAR)
    sexo = db.Column('sexo', db.CHAR)
    telefono = db.Column('telefono', db.VARCHAR)
    fecha_nacimiento = db.Column('fecha_nacimiento', db.DateTime)
    direccion = db.Column('direccion', db.VARCHAR)
    provincia = db.Column('provincia', db.VARCHAR)
    fechaAlta = db.Column('fechaAlta', db.DateTime)

    def __init__(self, nombres, ciudad, sexo, telefono, fecha_nacimiento, direccion, provincia):
        self.nombres = nombres
        self.ciudad = ciudad
        self.sexo = sexo
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.provincia = provincia

