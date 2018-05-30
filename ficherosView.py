from flask import Blueprint, jsonify, request
import json
from models.fichero import Fichero
from models.dbFlaskLink import db
from redisApp import r

bp_ficheros = Blueprint('bp_ficheros', __name__)


@bp_ficheros.route('/ficheros',methods=['GET'])
def getAllFicheros():
    data = Fichero.query.all()
    arrayData= []
    for i in data:
        arrayData.append({'id':i.id,'nombre':i.nombre,'tipo':i.tipo,'id_Vehiculo':i.id_Vehiculo})
        r.set('fichero:{}'.format(i.id), json.dumps(arrayData[len(arrayData)-1]))
    return json.dumps(arrayData)

#todos los recursos de 1 registro concreto
@bp_ficheros.route('/vehiculos/<int:vehiculoId>/ficheros', methods=['GET'])
def getAllFicherosFromVehiculo(vehiculoId):
    data = Fichero.query.filter_by(id_Vehiculo=vehiculoId)
    arrayData = []
    for i in data:
        arrayData.append({'id':i.id,'nombre':i.nombre,'tipo':i.tipo,'id_Vehiculo':i.id_Vehiculo})
    return json.dumps(arrayData)


#single file
@bp_ficheros.route('/fichero/<int:fileId>', methods=['GET'])
def getOneFileById(fileId):
    if r.exists('fichero:{}'.format(fileId)):
        return r.get('fichero:{}'.format(fileId))
    else:
        data = Fichero.query.filter_by(id=fileId)
        arrayData = []
        arrayData.append({'id':data[0].id,'nombre':data[0].nombre,'tipo':data[0].tipo,'id_Vehiculo':data[0].id_Vehiculo})
        r.set('fichero:{}'.format(fileId), json.dumps(arrayData))
        return json.dumps(arrayData)


#POST
@bp_ficheros.route('/ficheros', methods = ['POST'])
def addFichero():
    #TEST COMMAND = curl -i -d '{"nombre":"POSTPRUEBA","tipo":"FacturaPOST","id_Vehiculo":1}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/ficheros
    nombre = request.get_json(force=True)['nombre']
    tipo = request.get_json(force=True)['tipo']
    id_Vehiculo = request.get_json(force=True)['id_Vehiculo']

    nuevo = Fichero(nombre, tipo, id_Vehiculo)
    db.session.add(nuevo)
    db.session.commit()
    if nuevo.id > 0:
        r.set('fichero:{}'.format(nuevo.id), json.dumps([{'id':nuevo.id,'nombre':nombre,'tipo':tipo,'id_Vehiculo':id_Vehiculo}]))

    return "INSERTADO"


#PUT
@bp_ficheros.route('/ficheros', methods = ['PUT'])
def updateFichero():
    #TEST COMMAND = curl -i -d '{"id":19,"nombre":"POSTPRUEBA","tipo":"FacturaPOST","id_Vehiculo":1}' -H "Content-Type: application/json" -X PUT 127.0.0.1:8080/ficheros

    id = request.get_json(force=True)['id']
    editar = Fichero.query.filter_by(id=id).first()
    editar.nombre = request.get_json(force=True)['nombre']
    editar.tipo = request.get_json(force=True)['tipo']
    editar.id_Vehiculo = request.get_json(force=True)['id_Vehiculo']
    editar.data = "updated!"
    db.session.commit()

    r.set('fichero:{}'.format(id), json.dumps([{'id':id,'nombre':editar.nombre,'tipo':editar.tipo,'id_Vehiculo':editar.id_Vehiculo}]))

    return "EDITADO"


#DELETE
@bp_ficheros.route('/ficheros', methods = ['DELETE'])
def deleteFichero():
    #TEST COMMAND = curl -i -d '{"id":19}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/ficheros

    id = request.get_json(force=True)['id']
    borrar = Fichero.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    r.delete('fichero:{}'.format(id))

    return "BORRADO"
