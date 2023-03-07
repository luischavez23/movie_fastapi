from fastapi import FastAPI
from fastapi import HTTPException

from database import User
from database import Movie
from database import Review

from database import db_postgres as conn

from schema import UserRequestModel
from schema import UserResponseModel
from schema import MovieRequestModel
from schema import MovieResponseModel
from schema import ReviewRequestModel
from schema import ReviewResponseModel
from schema import UpdateReviewModel

from typing import List

app = FastAPI(
               title='Movies with FastAPI',
               description=' Make a Movie API with FastAPI',
               version=1.0)

@app.get('/')
async def index():
    return {
        'Hello':'World!'
    }

@app.on_event("startup")
async def startup_event():
    if conn.is_closed():
        conn.connect()
    conn.create_tables([User, Movie, Review])


@app.on_event("shutdown")
async def shutdown_event():
    if not conn.is_closed():
        conn.close()

# --------------- Create a new user ---------------

@app.post('/users', response_model=UserResponseModel)
async def create_user(user:UserRequestModel):
    
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'The username has already used.')
    
    hash_password = User.encrypted_password(user.password)

    user = User.create(
        username = user.username,
        password = hash_password
    )

    return user

@app.get('/users', response_model=List[UserResponseModel])
async def get_users():

    users = User.select()

    return [user for user in users]

# --------------- Create a new movie ---------------

@app.post('/movies', response_model=MovieResponseModel)
async def create_movie(movie:MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(409, 'The Movie has already used.')
    
    movie = Movie.create(
        title=movie.title
    )

    return movie

@app.get('/movies', response_model=List[MovieResponseModel])
async def get_movies():

    movies = Movie.select()

    return [movie for movie in movies]

@app.get('/movies/{movie_id}', response_model=MovieResponseModel)
async def get_movie(movie_id: int):
    
    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    return movie

# --------------- Create a new review ---------------

@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(review: ReviewRequestModel):

    if User.select().where( User.id == review.user_id ).first() is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    if Movie.select().where( Movie.id == review.movie_id ).first() is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    review = Review.create(
        user_id = review.user_id,
        movie_id = review.movie_id,
        description = review.description,
        rating = review.rating
    )
    
    return review

@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews():
    
    reviews = Review.select()

    return [review for review in reviews]

@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    
    review = Review.select().where(Review.id == review_id ).first()
    
    if review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    return review

@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id:int, review_request:UpdateReviewModel):
    
    review = Review.select().where(Review.id == review_id ).first()

    if review is None:
        raise HTTPException(status_code=404, detail='Review not found')

    review.description = review_request.description
    review.score = review_request.score
    
    review.save()
    
    return review

@app.delete('/reviews/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id:int):

    review = Review.select().where(Review.id == review_id).first()

    if review is None:
        return HTTPException(status_code=404, detail='Review not found')
    
    review.delete_instance()
    
    return review



