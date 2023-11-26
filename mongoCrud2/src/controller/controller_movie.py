import pandas as pd
from reports.relatorios import Relatorio
from model.movie import Movie
from conexion.mongo_queries import MongoQueries

class Controller_Movie:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_movie   (self) -> Movie:
        try:
            self.mongo.connect()

            movie_name = input("Nome do filme (Novo): ")

            if self.verifica_existencia_movie(movie_name):
                proximo_movie = self.mongo.db["movies"].aggregate([
                                                        {
                                                            '$group': {
                                                                '_id': '$movies', 
                                                                'proximo_movie': {
                                                                    '$max': '$movie_id'
                                                                }
                                                            }
                                                        }, {
                                                            '$project': {
                                                                'proximo_movie': {
                                                                    '$sum': [
                                                                        '$proximo_movie', 1
                                                                    ]
                                                                }, 
                                                                '_id': 0
                                                            }
                                                        }
                                
                                                ])
                

                proximo_movie_list = list(proximo_movie)

                if proximo_movie_list:
                    proximo_movie = int(proximo_movie_list[0]['proximo_movie'])
                else:
                    proximo_movie = 1

        
                movie_description = input("Descrição do filme: ")
                movie_priece = int(input("Preço do filme: "))
                
                self.relatorio.get_relatorio_movies_type()

                id = int(input("Digite o ID do genero: (Novo)"))
                

                df_movie_type = self.recupera_movie_type(id)

                movie_type_id = df_movie_type.movie_type_id.values[0]
                movie_genero = df_movie_type.movie_type_name.values[0]

                self.mongo.db["movies"].insert_one({
                    "movie_name": movie_name,
                    "movie_id": proximo_movie,
                    "movie_type_id": f"{movie_type_id}",
                    "movie_genero": f"{movie_genero}",
                    "movie_description": f"{movie_description}",
                    "movie_priece": movie_priece
                })
            
                df_movie = self.recupera_movie(movie_name)

                print(df_movie.to_string())

                novo_movie = Movie(df_movie.movie_id.values[0],df_movie.movie_type_id.values[0], df_movie.movie_genero.values[0], df_movie.movie_name.values[0], df_movie.movie_description.values[0], df_movie.movie_priece.values[0])
                print(novo_movie.to_string())
                self.mongo.close()
            
                return novo_movie
            else:
                self.mongo.close()
                print(f"O filme de ID {movie_name} já está cadastrado.")
                return None
        except ValueError:
            print("Valor inválido")

    def atualizar_movie(self) -> Movie:
        try:
            self.mongo.connect()
            self.relatorio.get_relatorio_movies()

            movie_name = input("nome do filme que deseja alterar: ")
            if not self.verifica_existencia_movie(movie_name):
                new_name = input("Novo nome: ")
                description = input("Nova descrição: ")
                priece = int(input("Novo preço: "))

                
                
                self.mongo.db["movies"].update_one({"movie_name": f"{movie_name}"}, {"$set": {"movie_name": f"{new_name}","description": f"{description}", "movie_priece": priece}})
                df_movie = self.recupera_movie(new_name)

                print(df_movie.to_string())

                movie_atualizado = Movie(df_movie.movie_id.values[0],df_movie.movie_type_id.values[0],df_movie.movie_name.values[0] , df_movie.movie_genero.values[0], df_movie.movie_description.values[0], df_movie.movie_priece.values[0])
                print(movie_atualizado.to_string())
                self.mongo.close()
                return movie_atualizado
            else:
                self.mongo.close()
                print(f"O CPF {movie_name} não existe.")
                return None
        except ValueError:
            print("Valor inválido") 



    def recupera_movie(self, movie_name:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_movie = pd.DataFrame(self.mongo.db["movies"].find({"movie_name":f"{movie_name}"}, {"movie_id": 1, "movie_type_id": 1, "movie_genero": 1, "movie_name": 1, "movie_description": 1, "movie_priece": 1, "_id": 0}))
        
        if external:
            self.mongo.close()

        return df_movie

    def verifica_existencia_movie(self, movie_name:str=None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_movie = pd.DataFrame(self.mongo.db["movies"].find({"movie_name":f"{movie_name}"}, {"movie_id": 1, "movie_type_id": 1, "movie_genero": 1, "movie_name": 1, "movie_description": 1, "movie_priece": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_movie.empty
    
    def recupera_movie_type(self, movie_name:str=None) -> pd.DataFrame:
        mongo = MongoQueries()
        mongo.connect()
        df_movie_type = pd.DataFrame(list(self.mongo.db["movies_type"].find({"movie_type_id": movie_name}, {"movie_type_id": 1, "movie_type_name": 1, "_id": 0})))
        mongo.close()

        return df_movie_type
        
    
  
