from model.movie import Movie
from model.users import User
class User_movie:
    def __init__(self,
                 user_movie_id:str=None,
                 user_id:str=None,
                 movie_id:str=None,
                ):
        self.set_user_movie_id(user_movie_id)
        self.set_user_id(user_id)
        self.set_movie_id(movie_id)
     

    def set_user_movie_id(self, user_movie_id:str):
        self.user_movie_id  = user_movie_id
    
    def set_user_id(self, user_id:str):
        self.user_id  = user_id
    
    def set_movie_id(self, movie_id:str):
        self.movie_id  = movie_id 



    def get_user_movie_id(self) -> str:
        return self.user_movie_id

    def get_user_id(self) -> str:
        return self.user_id    
    
    def get_movie_id(self) -> str:
        return self.movie_id    

    
    def to_string(self) -> str:
        return f"ID: {self.get_user_movie_id()} | UserID: {self.get_user_id()} | Movie_ID: {self.get_movie_id()}"