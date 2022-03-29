from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.album import Album
from flask import render_template,redirect,request, session

# CREATE

@app.route("/create/post", methods=['POST'])
def create_album():
    if not Album.validate_album(request.form):
        return redirect('/albums/new')
    data = {
        "name": request.form['name'],
        "artist": request.form['artist'],
        "release_date": request.form['release_date'],
        "favorite_tracks": request.form['favorite_tracks'],
        "user_id": session['user_id']
    }
    Album.save(data)
    return redirect('/dashboard')

# READ

@app.route('/albums/new')
def add_album():
    return render_template("create_album.html")

@app.route('/album/<int:id>')
def display_album(id):
    Album.get_liked_albums({"id": id})
    Album.get_unliked_albums({"id": id})
    return render_template("view_album.html", albums = Album.get_liked_albums({"id": id}), unliked_albums = Album.get_unliked_albums({"id": id}))

@app.route("/albums/like/<int:id>")
def like_album(id):
    # Go to db, add album id and user id to like table.
    data = {
        "album_id": id,
        "user_id": session["user_id"]
    }
    Album.like_album(data)
    return redirect("/dashboard") 

# UPDATE

@app.route('/albums/edit/<int:id>')
def edit_album(id):
    album_to_edit = Album.get_one({"id": id})
    return render_template("edit_album.html", album = album_to_edit)

@app.route('/edit/post', methods=['POST'])
def update_album():
    if not Album.validate_album(request.form):
        return redirect('/albums/new')
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "artist": request.form['artist'],
        "release_date": request.form['release_date'],
        "favorite_tracks": request.form['favorite_tracks'],
        "user_id": session['user_id']
    }
    Album.update(data)
    return redirect('/dashboard')

# DELETE

@app.route('/albums/delete/<int:id>')
def delete_album(id):
    Album.destroy({"id": id})
    return redirect('/dashboard')
