from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from config.database import Session, engine, Base
from models import Movie

class Movie (BaseModel):
    title : str
    overview : str 
    year : int 
    rating : float | None = None
    category : str

#Creación de la API 
app = FastAPI()
app.title = "Mi aplicación de FastaAPI"
app.version = "1.1.0"

Base.metada.create_all( bind = engine )


#Creación del endpoint con la ruta
@app.get('/', tags=['home'])

#función que se va a ejecutar
def message():
    return HTMLResponse('<h1> Hello world </h1>')

@app.get('/movies', tags= ['movies'])
def getMovies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
async def get_movie(id : int ) -> list:
    movie = list(filter(lambda movie: movie['id']== id, movies)) 
    return movie

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category : str):
    return  [movie for movie in movies if str.lower(movie['category']) == str.lower(category)]

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(),  rating:float = Body(), category: str = Body()):
    movies.append( {
        "id" : id,
        "title": title,
        "overview" : overview,
        "year" : year,
        "rating": rating,
        "category": category
    })
    return movies
    
#Actualización de películas
@app.put( "/movies/{movie_id}" , tags = ['movies'], response_model = Movie )
async def update_movie(movie_id: int, new_movie: Movie ):
    update_movie_encoded = jsonable_encoder(new_movie)
    movies[movie_id] = update_movie_encoded
    return update_movie_encoded


#Eliminación de películas

@app.delete( "/movie/{movie_id}", tags=['movies'], response_model = Movie )
async def delete_movie (movie_id: int):
    return movies.pop(movie_id)