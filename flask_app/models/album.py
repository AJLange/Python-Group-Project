from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash


class Album:
    db = ("fav_albums")

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.artist = data['artist']
        self.release_date = data['release_date']
        self.favorite_tracks = data['favorite_tracks']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.liked_by = []
        self.user = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO albums (name,artist,release_date,favorite_tracks,user_id) VALUES (%(name)s,%(artist)s,%(release_date)s,%(favorite_tracks)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM albums WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE albums SET name=%(name)s, artist=%(artist)s, release_date=%(release_date)s, favorite_tracks=%(favorite_tracks)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM albums JOIN users ON albums.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        albums = []
        for row in results:
            this_album = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row['email'],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            this_user = User(user_data)
            this_album.user.append(this_user)
            albums.append(this_album)
        return albums

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM albums JOIN users ON albums.user_id = users.id WHERE albums.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        user_data = {
            "id" : row['users.id'],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row['email'],
            "password": row["password"],
            "created_at": row["users.created_at"],
            "updated_at": row["users.updated_at"]
        }
        this_user = User(user_data)
        row['user'] = this_user
        return cls(row)

    @classmethod
    def get_liked_albums(cls,data):
        query = "SELECT * from albums WHERE albums.id IN (SELECT album_id FROM likes WHERE user_id = %(id)s );"
        results =connectToMySQL(cls.db).query_db(query,data)
        albums = []
        for row in results:
            albums.append(cls(row))
        print(albums)
        return albums

    @classmethod
    def get_unliked_albums(cls,data):
        query = "SELECT * from albums WHERE albums.id NOT IN (SELECT album_id FROM likes WHERE user_id = %(id)s );"
        results =connectToMySQL(cls.db).query_db(query,data)
        albums = []
        for row in results:
            albums.append(cls(row))
        print(albums)
        return albums

    @classmethod
    def like_album(cls, data):
        query = "INSERT INTO likes (user_id,album_id) VALUES (%(user_id)s,%(album_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

 
    @staticmethod
    def validate_album(album):
        is_valid = True
        if len(album['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", "album")
        if len(album['artist']) < 3:
            is_valid = False
            flash("Artist names' must be at least 3 characters", "album")
        if album['release_date'] == "":
            is_valid = False
            flash("Please enter a date", "album")
        if len(album['favorite_tracks']) < 3:
            is_valid = False
            flash("Favorite tracks must be at least 3 characters", "album")
        return is_valid
