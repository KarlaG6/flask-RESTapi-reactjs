from peewee import *
import datetime

DATABASE = MySQLDatabase('REST', host='localhost', user='root', passwd='toor')

class Song(Model):
    class Meta:
        database = DATABASE
        db_table = 'Song'

    title = CharField(unique=False, max_length=250)
    author = CharField(unique=False, max_length=250)
    version = TextField()
    created_at = DateTimeField(default = datetime.datetime.now())

    # Se pasan los campos que se quieren mostrar en la api
    def to_json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'version': self.version}

def create_song():
    title = 'Lost Woods'
    author = 'Zelda'
    version = 'Zelda & Chill'
    # verificamos que el titulo todavia no exista antes de crearlo pues title debe ser unico
    if not Song.select().where(Song.title == title):
        Song.create(title=title, author=author, version=version)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables( [Song], safe=True)
    create_song()
    DATABASE.close()