from flask import Blueprint, jsonify, request
import json
from models.cliente import Cliente
from models.dbFlaskLink import db
from redisApp import r

bp_clientes = Blueprint('bp_clientes', __name__)

@bp_clientes.route('/clientes', methods=['GET'])
def getAllClientes():
    #aqui redis hay un problema, redis guarda por key:value, si guardo todos los valores luego como sé hasta que valor deberia recorrer con redis?... tendria que guardar la id maxima
    # lo que voy hacer es, si se hace un get a todos los recursos de un tipo, copiar todos los recursos a redis y si luego se hace request a recursos unicos ya los tengo, problema? si hago peticiones un getAllClientes una y otra vez, estare sobreescribiendo datos que ya existen y que quiza sea identicos
    data = Cliente.query.all()
    arrayData = []
    for i in data:
        arrayData.append({'id':i.id,'nombres':i.nombres,'ciudad':i.ciudad,'sexo':i.sexo,'telefono':i.telefono,'fecha_nacimiento':i.fecha_nacimiento.strftime("%Y-%m-%d %H:%M:%S"),'direccion':i.direccion,'provincia':i.provincia,'fechaAlta':i.fechaAlta.strftime("%Y-%m-%d %H:%M:%S")})
        #guardo en redis 1 a 1
        r.set('cliente:{}'.format(i.id), json.dumps([{'id':i.id,'nombres':i.nombres,'ciudad':i.ciudad,'sexo':i.sexo,'telefono':i.telefono,'fecha_nacimiento':i.fecha_nacimiento.strftime("%Y-%m-%d %H:%M:%S"),'direccion':i.direccion,'provincia':i.provincia,'fechaAlta':i.fechaAlta.strftime("%Y-%m-%d %H:%M:%S")}]))
    return json.dumps(arrayData)


#1 registro por concreto
@bp_clientes.route('/cliente/<int:id>', methods = ['GET'])
def getOneClient(id):
    if r.exists('cliente:{}'.format(id)):
        return r.get('cliente:{}'.format(id))
    else:
        data = Cliente.query.filter_by(id=id)
        arrayData = []
        arrayData.append({'id':data[0].id,'nombres':data[0].nombres,'ciudad':data[0].ciudad,'sexo':data[0].sexo,'telefono':data[0].telefono,'fecha_nacimiento':data[0].fecha_nacimiento.strftime("%Y-%m-%d %H:%M:%S"),'direccion':data[0].direccion,'provincia':data[0].provincia,'fechaAlta':data[0].fechaAlta.strftime("%Y-%m-%d %H:%M:%S")})
        r.set('cliente:{}'.format(id), json.dumps(arrayData))
        return json.dumps(arrayData)


#POST cliente
@bp_clientes.route('/nuevo/cliente', methods = ['POST'])
def addCliente():
    #TEST COMMAND = curl -i -d '{"nombres":"testiee","ciudad":"Granada","sexo":"M","telefono":"123321123","fecha_nacimiento":"2000-06-23","direccion":"una random","provincia":"ninguna"}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/nuevo/cliente
    nombre = request.get_json(force=True)['nombres']
    ciudad = request.get_json(force=True)['ciudad']
    sexo = request.get_json(force=True)['sexo']
    telefono = request.get_json(force=True)['telefono']
    fecha_nacimiento = request.get_json(force=True)['fecha_nacimiento']
    direccion = request.get_json(force=True)['direccion']
    provincia = request.get_json(force=True)['provincia']

    nuevo = Cliente(nombre,ciudad,sexo,telefono,fecha_nacimiento,direccion, provincia)
    db.session.add(nuevo)
    db.session.commit()
    
    # si se ha insertado, meter en redis
    if nuevo.id > 0:
        r.set('cliente:{}'.format(nuevo.id), json.dumps([{"id":nuevo.id,"nombres":nuevo.nombres,"ciudad":nuevo.ciudad,"sexo":nuevo.sexo,"telefono":nuevo.telefono,"fecha_nacimiento":fecha_nacimiento,"direccion":nuevo.direccion,"provincia":nuevo.provincia, 'fechaAlta':nuevo.fechaAlta.strftime("%Y-%m-%d %H:%M:%S")}]))
    return "Cliente insertado con ID : {}".format(nuevo.id)


#PUT cliente
@bp_clientes.route('/editar/cliente', methods = ['PUT'])
def updateCliente():
    #TEST COMMAND = curl -i -d '{"id":6,"nombres":"testiee","ciudad":"Granada","sexo":"M","telefono":"123321123","fecha_nacimiento":"2000-06-23","direccion":"una random","provincia":"ninguna"}' -H "Content-Type: application/json" -X PUT 127.0.0.1:8080/editar/cliente
    id = request.get_json(force=True)['id']
    editar = Cliente.query.filter_by(id=id).first()
    editar.nombres = request.get_json(force=True)['nombres']
    editar.ciudad = request.get_json(force=True)['ciudad']
    editar.sexo = request.get_json(force=True)['sexo']
    editar.telefono = request.get_json(force=True)['telefono']
    editar.fecha_nacimiento = request.get_json(force=True)['fecha_nacimiento']
    editar.direccion = request.get_json(force=True)['direccion']
    editar.provincia = request.get_json(force=True)['provincia']
    editar.data = "updated!"

    # lo suyo seria poner en try exception block esto asi si peta el commit no edito redis
    # además, esta puesto que se pueda sobreescribir el registro de redis, habria que ver lo mejor, si borrarlo y crear otro, o dejarlo asi y poder sobreescribir registros..
    db.session.commit()
    r.set('cliente:{}'.format(id), json.dumps([{"id":id,"nombres":editar.nombres,"ciudad":editar.ciudad,"sexo":editar.sexo,"telefono":editar.telefono,"fecha_nacimiento":editar.fecha_nacimiento.strftime("%Y-%m-%d %H:%M:%S"),"direccion":editar.direccion,"provincia":editar.provincia, 'fechaAlta':editar.fechaAlta.strftime("%Y-%m-%d %H:%M:%S")}]))

    return "Cliente editado"


#DELETE cliente
@bp_clientes.route('/borrar/cliente', methods = ['DELETE'])
def deleteClient():
    #TEST COMMAND = curl -i -d '{"id":13}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/borrar/cliente
    id = request.get_json(force=True)['id']
    borrar = Cliente.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    r.delete('cliente:{}'.format(id))

    return "Cliente borrado"

