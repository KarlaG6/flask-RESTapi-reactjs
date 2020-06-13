from flask import Flask, g, jsonify, abort, request
from models import initialize, Song, DATABASE

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
def wrong_request():
  return jsonify( generate_response(400, error='Necesitas parametros'))

@app.route('/code/api/v1.0/songs', methods=['GET'])
def get_songs():
  songs = Song.select()
  songs = [ song.to_json() for song in songs ]
  return jsonify( generate_response( data = songs) )

@app.route('/code/api/v1.0/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
  song = try_song(song_id)
  return jsonify( generate_response( data = song.to_json()) )

@app.route('/code/api/v1.0/songs/')
def post_song():
  if not request.json:
    abort(400)
    # 400 = mal request
  return "Ok"
  
def generate_response(status = 200, data = None, error = None):
  return {'status': status, 'data': data, 'error': error}

def try_song(song_id):
  try:
    return Song.get(Song.id == song_id)
  except Song.DoesNotExist:
    abort(404)

if __name__ == '__main__':
  initialize()
  app.run(host='127.0.0.1', port=8000, debug=DEBUG)