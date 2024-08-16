from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)

# Create tables on app startup
def create_tables():
    with app.app_context():
        db.create_all()

# Home route to list movies
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

# Route to stream a movie
@app.route('/watch/<int:movie_id>')
def watch(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('watch.html', movie=movie)

# Route to serve the movie file
@app.route('/stream/<path:filename>')
def stream(filename):
    return send_file(filename, as_attachment=False)

# Add movie route (for simplicity, using a basic form)
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = request.form['year']
        description = request.form['description']
        filepath = request.form['filepath']

        new_movie = Movie(title=title, director=director, year=year, description=description, filepath=filepath)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_movie.html')

if __name__ == '__main__':
    create_tables()  # Manually create tables on app startup
    app.run(debug=True)
