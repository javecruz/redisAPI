from flask import Blueprint, jsonify

account_api = Blueprint('account_api', __name__)

@account_api.route('/', methods=['GET'])
def test():
    return jsonify({'info' : 'API REST - VELANDO CRUZ, JAVIER'})

