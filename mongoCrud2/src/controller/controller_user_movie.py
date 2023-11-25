import pandas as pd
from model.user_movie import User_movie
from reports.relatorios import Relatorio
from conexion.mongo_queries import MongoQueries

class Controller_User_movie:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
    
    def inserir_user_movie(self) -> User_movie:
        try:
            self.mongo.connect()

            self.relatorio.get_relatorio_users()

            user_id = int(input("ID do usuário comprador (Novo): "))
            
            if  self.verifica_existencia_user(user_id):
                proximo_user_movie = self.mongo.db["user_movie"].aggregate([
                                                        {
                                                            '$group': {
                                                                '_id': '$user_movie', 
                                                                'proximo_user_movie': {
                                                                    '$max': '$user_movie_id'
                                                                }
                                                            }
                                                        }, {
                                                            '$project': {
                                                                'proximo_user_movie': {
                                                                    '$sum': [
                                                                        '$proximo_user_movie', 1
                                                                    ]
                                                                }, 
                                                                '_id': 0
                                                            }
                                                        }
                                                    ])
                

                proximo_user_movie_list = list(proximo_user_movie)

                if proximo_user_movie_list:
                    proximo_user_movie = int(proximo_user_movie_list[0]['proximo_user_movie'])
                else:
                    proximo_user_movie = 1  
        
                self.relatorio.get_relatorio_movies()
                movie_id = int(input("ID do filme a ser vendido (Novo): "))
            
                self.mongo.db["user_movie"].insert_one({"user_movie_id": proximo_user_movie ,"movie_id": movie_id, "user_id": user_id})
            
                df_user_movie = self.recupera_user_movie(proximo_user_movie)


                novo_user_movie = User_movie(df_user_movie.user_movie_id.values[0],df_user_movie.user_id.values[0], df_user_movie.movie_id.values[0])
                print(novo_user_movie.to_string())
                self.mongo.close()
            
                return novo_user_movie
            else:
                self.mongo.close()
                print(f"O Usuário não existe.")
                return None
        except ValueError:
            print("Valor inválido") 

    def recupera_user_movie(self, user_movie_id:int=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_user_movie = pd.DataFrame(list(self.mongo.db["user_movie"].find({"user_movie_id": user_movie_id}, {"user_movie_id": 1,"user_id":1, "movie_id":1, "_id": 0})))
        
        if external:
            self.mongo.close()

        return df_user_movie

    def verifica_existencia_user(self, user_id:str=None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_user = pd.DataFrame(self.mongo.db["users"].find({"user_id":f"{user_id}"}, {"user_fullname": 1, "telephone": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_user.empty
    
   