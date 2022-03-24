from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app


class Album:
    db = ("fav_albums")
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.artist = data['artist']
        self.release_date= data['release_date']
        self.favorite_tracks = data['favorite_tracks']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM albums;"
        results = connectToMySQL(Album.db).query_db(query)
        albums = []
        for a in results:
            albums.append(cls(a))
        return albums