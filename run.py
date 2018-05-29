from flask import Flask, jsonify, request
from datetime import datetime
import json
from models.dbFlaskLink import db
from models.cliente import Cliente
from models.fichero import Fichero
from models.vehiculo import Vehiculo
#all config info such db
import config
# redis connection
from redisApp import r

app = Flask(__name__)
app.config[config.key] = config.url

# inicio db con la app de flask asi la tienen los modelos
db.init_app(app)

@app.route('/', methods=['GET'])
def test():
    return jsonify({'info' : 'API REST - VELANDO CRUZ, JAVIER'})

# todos los recursos
@app.route('/clientes', methods=['GET'])
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


@app.route('/ficheros',methods=['GET'])
def getAllFicheros():
    data = Fichero.query.all()
    arrayData= []
    for i in data:
        arrayData.append({'id':i.id,'nombre':i.nombre,'tipo':i.tipo,'id_Vehiculo':i.id_Vehiculo})
        r.set('fichero:{}'.format(i.id), json.dumps)
    return json.dumps(arrayData)

@app.route('/vehiculos', methods = ['GET'])
def getAllVehiculos():
    data = Vehiculo.query.all()
    arrayData = []
    
    for i in data: 
        arrayData.append({'id':i.id,'matricula':i.matricula,'fecha_fabricacion':i.fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"),'marca':i.marca,'modelo':i.modelo,'id_cliente':i.id_cliente,'Tipo':i.Tipo})
        r.set('vehiculo:{}'.format(i.id), json.dumps(arrayData))
    return json.dumps(arrayData)
    

#todos los recursos de 1 registro concreto
@app.route('/vehiculos/<int:vehiculoId>/ficheros', methods=['GET'])    
def getAllFicherosFromVehiculo(vehiculoId):
    data = Fichero.query.filter_by(id_Vehiculo=vehiculoId)
    arrayData = []
    #TOFIX
    for i in data:
        arrayData.append({'id':i.id,'nombre':i.nombre,'tipo':i.tipo,'id_Vehiculo':i.id_Vehiculo})
    return json.dumps(arrayData)

@app.route('/cliente/<int:clienteId>/vehiculos', methods = ['GET'])
def getAllVehiculosFromCliente(clienteId):
    data = Vehiculo.query.filter_by(id_cliente=clienteId)
    arrayData = []

    for i in data:
        arrayData.append({'id':i.id,'matricula':i.matricula,'fecha_fabricacion':i.fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"),'marca':i.marca,'modelo':i.modelo,'id_cliente':i.id_cliente,'Tipo':i.Tipo})
    return json.dumps(arrayData)

#1 registro por concreto
@app.route('/cliente/<int:id>', methods = ['GET'])
def getOneClient(id):
    if r.exists('cliente:{}'.format(id)):
        print('redisssss')
        return r.get('cliente:{}'.format(id))
    else:
        print('data baseeeee')
        data = Cliente.query.filter_by(id=id)
        arrayData = []
        arrayData.append({'id':data[0].id,'nombres':data[0].nombres,'ciudad':data[0].ciudad,'sexo':data[0].sexo,'telefono':data[0].telefono,'fecha_nacimiento':data[0].fecha_nacimiento.strftime("%Y-%m-%d %H:%M:%S"),'direccion':data[0].direccion,'provincia':data[0].provincia,'fechaAlta':data[0].fechaAlta.strftime("%Y-%m-%d %H:%M:%S")})
        r.set('cliente:{}'.format(id), json.dumps(arrayData))
        return json.dumps(arrayData)


@app.route('/fichero/<int:fileId>', methods=['GET'])
def getOneFileById(fileId):
    if r.exists('fichero:{}'.format(fileId)):
        print('redis')
        return r.get('fichero:{}'.format(fileId))
    else:
        print('data baseee')
        data = Fichero.query.filter_by(id=fileId)
        arrayData = []
        arrayData.append({'id':data[0].id,'nombre':data[0].nombre,'tipo':data[0].tipo,'id_Vehiculo':data[0].id_Vehiculo})
        r.set('fichero:{}'.format(fileId), json.dumps(arrayData))
        return json.dumps(arrayData)


@app.route('/vehiculo/<int:carId>', methods=['GET'])
def getOneCar(carId):
    if r.exists('vehiculo:{}'.format(carId)):
        #return from redis
        print('soy redis y te doy esto ------>>>>>')
        return r.get('vehiculo:{}'.format(carId))
    else:
        #return from DB
        data = Vehiculo.query.filter_by(id=carId)
        arrayData = []
    	#TOFIX, si pongo un id que no existe, peta, INDEX OUT OF ERROR
        arrayData.append({'id':data[0].id,'matricula':data[0].matricula,'fecha_fabricacion':data[0].fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"),'marca':data[0].marca,'modelo':data[0].modelo,'id_cliente':data[0].id_cliente,'Tipo':data[0].Tipo})
        #guardo en redis
        r.set('vehiculo:{}'.format(carId), json.dumps(arrayData))
        print('vengo de la DB y te doy esto') 
        return json.dumps(arrayData)



#POST
@app.route('/nuevo/cliente', methods = ['POST'])
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
    if nuevo.id > 0:
        r.set('cliente:{}'.format(nuevo.id), json.dumps([{"nombres":nuevo.nombres,"ciudad":nuevo.ciudad,"sexo":nuevo.sexo,"telefono":nuevo.telefono,"fecha_nacimiento":fecha_nacimiento,"direccion":nuevo.direccion,"provincia":nuevo.provincia, 'fechaAlta':nuevo.fechaAlta.strftime("%Y-%m-%d %H:%M:%S")}]))
    return "CLientee insertado con ID : {}".format(nuevo.id)



@app.route('/ficheros', methods = ['POST'])
def addFichero():
    #TEST COMMAND = curl -i -d '{"nombre":"POSTPRUEBA","tipo":"FacturaPOST","id_Vehiculo":1}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/ficheros
    nombre = request.get_json(force=True)['nombre']
    tipo = request.get_json(force=True)['tipo']
    id_Vehiculo = request.get_json(force=True)['id_Vehiculo']
    
    nuevo = Fichero(nombre, tipo, id_Vehiculo)
    db.session.add(nuevo)
    db.session.commit()
    if nuevo.id > 0:
        r.set('fichero:{}'.format(nuevo.id), json.dumps([{'nombre':nombre,'tipo':tipo,'id_Vehiculo':id_Vehiculo}]))
    
    #FIX this
    #return request.get_json(force=True)["nombre"]
    return "INSERTADO"


#data[0].fecha_fabricacion = data[0].fecha_fabricacion.replace(year=2012)
#test = datetime.strptime('2018-02-08', '%Y-%m-%d')
@app.route('/nuevo/vehiculo', methods = ['POST'])
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





#PUT
@app.route('/editar/cliente', methods = ['PUT'])
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
    r.set('cliente:{}'.format(id), json.dumps([{"nombres":editar.nombres,"ciudad":editar.ciudad,"sexo":editar.sexo,"telefono":editar.telefono,"fecha_nacimiento":editar.fecha_nacimiento.strftime("%Y-%m-%d %H:%M:%S"),"direccion":editar.direccion,"provincia":editar.provincia, 'fechaAlta':editar.fechaAlta.strftime("%Y-%m-%d %H:%M:%S")}]))


    return "Cliente editado"



@app.route('/ficheros', methods = ['PUT'])
def updateFichero():
    #TEST COMMAND = curl -i -d '{"id":19,"nombre":"POSTPRUEBA","tipo":"FacturaPOST","id_Vehiculo":1}' -H "Content-Type: application/json" -X PUT 127.0.0.1:8080/ficheros

    id = request.get_json(force=True)['id']
    editar = Fichero.query.filter_by(id=id).first()
    editar.nombre = request.get_json(force=True)['nombre']
    editar.tipo = request.get_json(force=True)['tipo']
    editar.id_Vehiculo = request.get_json(force=True)['id_Vehiculo']
    editar.data = "updated!"
    db.session.commit()
    
    r.set('fichero:{}'.format(id), json.dumps([{'nombre':editar.nombre,'tipo':editar.tipo,'id_Vehiculo':editar.id_Vehiculo}]))

    return "EDITADO"

@app.route('/editar/vehiculo', methods = ['PUT'])
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
    r.set('vehiculo:{}'.format(id), json.dumps([{'id':editar.id,'matricula':editar.matricula, 'fecha_fabricacion':editar.fecha_fabricacion.strftime("%Y-%m-%d %H:%M:%S"), 'marca':editar.marca, 'modelo':editar.modelo, 'id_cliente':editar.id_cliente, 'tipo':editar.Tipo}]))
 
    return "VEHICULO EDITADO"


#DELETE
@app.route('/borrar/cliente', methods = ['DELETE'])
def deleteClient():
    #TEST COMMAND = curl -i -d '{"id":5}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/borrar/cliente
    id = request.get_json(force=True)['id']
    borrar = Cliente.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    r.delete('cliente:{}'.format(id))

    return "Cliente borrado"

@app.route('/ficheros', methods = ['DELETE'])
def deleteFichero():
    #TEST COMMAND = curl -i -d '{"id":19}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/ficheros

    id = request.get_json(force=True)['id']
    borrar = Fichero.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    r.delete('fichero:{}'.format(id))
    
    return "BORRADO"

@app.route('/borrar/vehiculo', methods = ['DELETE'])
def deleteVehiculo():
    #TEST COMMAND = curl -i -d '{"id":13}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/borrar/vehiculo
    id = request.get_json(force=True)['id']
    borrar = Vehiculo.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    r.delete('vehiculo:{}'.format(id))

    return "Vehiculo Borrado"


if __name__ == '__main__':
   app.run(debug=True, port=8080)
