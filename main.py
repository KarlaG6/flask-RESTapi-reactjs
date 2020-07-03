from flask import Flask, g, jsonify, abort, request
from models import initialize, Song, DATABASE
import time

app = Flask(__name__)
DEBUG = True

@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()

@app.after_request
def after_request(request):
    g.db.close()
    return request

@app.errorhandler(404)
def not_found(error):
    return jsonify( generate_response(404, error='Cancion no encontrada'))

@app.errorhandler(400)
def wrong_request(error):
    return jsonify( generate_response(400, error='Necesitas parametros'))

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify( generate_response(422, error='Unprocessable entity'))

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/code/api/v1.0/songs', methods=['GET'])
def get_songs():
    songs = Song.select()
    songs = [ song.to_json() for song in songs ]
    return jsonify( generate_response( data = songs) )

@app.route('/code/api/v1.0/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = try_song(song_id)
    return jsonify( generate_response( data = song.to_json()) )

@app.route('/code/api/v1.0/songs/', methods=['POST']) 
def post_song():
    if not request.json:
        abort(400)

    title = request.json.get('title', '')
    author = request.json.get('author', '')
    version = request.json.get('version', '')

    song = Song.new( title, author, version)
    if song is None:
        abort(422)
    return jsonify( generate_response( data=song.to_json()))
    
# endpoint para update
@app.route('/code/api/v1.0/songs/<int:song_id>', methods=['PUT'])
def put_song(song_id):
    song = try_song(song_id)
    if not request.json:
        abort(400)
    song.title = request.json.get('title', song.title)
    song.author = request.json.get('author', song.author)
    song.version = request.json.get('version', song.version)

    # valida qu eel titulo no este en la BD
    if song.save():
        return jsonify( generate_response( data=song.to_json()))
    else:
        abort(422)


@app.route('/code/api/v1.0/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    song = try_song(song_id)
    if song.delete_instance():
        return jsonify( generate_response( data={}))
    else:
        abort(422)
def try_song(song_id):
    try:
        return Song.get(Song.id == song_id)
    except Song.DoesNotExist:
        abort(404)

def generate_response(status = 200, data = None, error = None):
    return {'status': status, 'data': data, 'error': error}
    
if __name__ == '__main__':
    initialize()
    app.run(host='127.0.0.1', port=8000, debug=DEBUG)


# falta: que solo los usuarios con unnivel avanzado puedan eliminar, crear y mod, tambien vaqlidar que dentro del request.json siempre vengan todos los atributos pedidos