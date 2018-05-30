from flask import Flask, jsonify
#la conexion para poder iniciarlizar la app de flask desde aqui
from models.dbFlaskLink import db
#views
from clientesView import bp_clientes
from vehiculosView import bp_vehiculos
from ficherosView import bp_ficheros
#all config info such db
import config
# redis connection
from redisApp import r

app = Flask(__name__)

# Registro de blueprints
app.register_blueprint(bp_clientes)
app.register_blueprint(bp_vehiculos)
app.register_blueprint(bp_ficheros)

#config de db connector y url
app.config[config.key] = config.url

# inicio db con la app de flask asi la tienen los modelos
db.init_app(app)

@app.route('/', methods=['GET'])
def test():
    return jsonify({'info' : 'API REST - VELANDO CRUZ, JAVIER','Curso':'DAW IES CONSELLERIA 2016-2017'})

#si este script se ha ejecutado de forma directa(es decir, no se ha importado) __name__ sera igual a __main__
if __name__ == '__main__':
   app.run(debug=True, port=8080)
