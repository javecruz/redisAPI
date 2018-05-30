from flask import Blueprint, jsonify, request
import json
from models.vehiculo import Vehiculo
from models.dbFlaskLink import db
from redisApp import r

bp_vehiculos = Blueprint('bp_vehiculos', __name__)

@bp_vehiculos.route('/vehiculos', methods = ['GET'])
def getAllVehiculos():
    data = Vehiculo.query.all()
    arrayData = []

    for i in data:
        arrayData.append({'id':i.id,'matricula':i.matricula,'fecha_fabricacion':i.fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"),'marca':i.marca,'modelo':i.modelo,'id_cliente':i.id_cliente,'Tipo':i.Tipo})
        r.set('vehiculo:{}'.format(i.id), json.dumps(arrayData[len(arrayData)-1]))
    return json.dumps(arrayData)


@bp_vehiculos.route('/cliente/<int:clienteId>/vehiculos', methods = ['GET'])
def getAllVehiculosFromCliente(clienteId):
    data = Vehiculo.query.filter_by(id_cliente=clienteId)
    arrayData = []

    for i in data:
        arrayData.append({'id':i.id,'matricula':i.matricula,'fecha_fabricacion':i.fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"),'marca':i.marca,'modelo':i.modelo,'id_cliente':i.id_cliente,'Tipo':i.Tipo})
    return json.dumps(arrayData)


@bp_vehiculos.route('/vehiculo/<int:carId>', methods=['GET'])
def getOneCar(carId):
    if r.exists('vehiculo:{}'.format(carId)):
        #return from redis
        return r.get('vehiculo:{}'.format(carId))
    else:
        #return from DB
        data = Vehiculo.query.filter_by(id=carId)
        arrayData = []
        arrayData.append({'id':data[0].id,'matricula':data[0].matricula,'fecha_fabricacion':data[0].fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"),'marca':data[0].marca,'modelo':data[0].modelo,'id_cliente':data[0].id_cliente,'Tipo':data[0].Tipo})
        #guardo en redis
        r.set('vehiculo:{}'.format(carId), json.dumps(arrayData))
        return json.dumps(arrayData)


#POST
@bp_vehiculos.route('/nuevo/vehiculo', methods = ['POST'])
def addVehiculo():
    #TEST COMMAND = curl -i -d '{"matricula":"1233-JU","fecha_fabricacion":"2018-02-08","marca":"Ford","modelo":"focus","id_cliente":1,"Tipo":2}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/nuevo/vehiculo
    matricula = request.get_json(force=True)['matricula']
    fecha = request.get_json(force=True)['fecha_fabricacion']
    marca = request.get_json(force=True)['marca']
    modelo = request.get_json(force=True)['modelo']
    id_cliente = request.get_json(force=True)['id_cliente']
    tipo = request.get_json(force=True)['Tipo']

    nuevo = Vehiculo(matricula, fecha, marca, modelo, id_cliente, tipo)
    db.session.add(nuevo)
    db.session.commit()

    if nuevo.id > 0:
        r.set('vehiculo:{}'.format(nuevo.id), json.dumps([{'id':nuevo.id,'matricula':matricula, 'fecha_fabricacion':fecha, 'marca':marca, 'modelo':modelo, 'id_cliente':id_cliente, 'tipo':tipo}]))

    return "Vehiculo Insertado con ID = {}".format(nuevo.id)


#PUT vehiculo
@bp_vehiculos.route('/editar/vehiculo', methods = ['PUT'])
def updateVehiculo():
    #TEST COMMAND = curl -i -d '{"id":12,"matricula":"1233-JU","fecha_fabricacion":"2018-02-08","marca":"Ford","modelo":"focus","id_cliente":1,"Tipo":2}' -H "Content-Type: application/json" -X PUT 127.0.0.1:8080/editar/vehiculo

    id = request.get_json(force=True)['id']
    editar = Vehiculo.query.filter_by(id=id).first()
    editar.matricula = request.get_json(force=True)['matricula']
    editar.fecha_fabricacion = request.get_json(force=True)['fecha_fabricacion']
    editar.marca = request.get_json(force=True)['marca']
    editar.modelo = request.get_json(force=True)['modelo']
    editar.id_cliente = request.get_json(force=True)['id_cliente']
    editar.Tipo = request.get_json(force=True)['Tipo']
    editar.data = "updated!"
    db.session.commit()
    r.set('vehiculo:{}'.format(id), json.dumps([{'id':id,'matricula':editar.matricula, 'fecha_fabricacion':editar.fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"), 'marca':editar.marca, 'modelo':editar.modelo, 'id_cliente':editar.id_cliente, 'tipo':editar.Tipo}]))

    return "VEHICULO EDITADO"


#DELETE
@bp_vehiculos.route('/borrar/vehiculo', methods = ['DELETE'])
def deleteVehiculo():
    #TEST COMMAND = curl -i -d '{"id":13}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/borrar/vehiculo
    id = request.get_json(force=True)['id']
    borrar = Vehiculo.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    r.delete('vehiculo:{}'.format(id))

    return "Vehiculo Borrado"

