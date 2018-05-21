import redis

#redis connection, server should be running on background
#tal como viene por defecto, si hago un set a algo que ya existe, se chafa, se puede evitar cambiando configuración o con r.exists('foo')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

