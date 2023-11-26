import pandas as pd
from model.movie_type import MovieType
from conexion.mongo_queries import MongoQueries
from reports.relatorios import Relatorio


class Controller_MovieType:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()

   
    def inserir_movie_type(self) -> MovieType:
            try:
                self.mongo.connect()

                movie_type = str(input("genêro do filme (Novo): "))

                if self.recupera_movie_typeByName(movie_type).empty:
                    proximo_movie_type = self.mongo.db["movies_type"].aggregate([
                                                            {
                                                                '$group': {
                                                                    '_id': '$movies_type', 
                                                                    'proximo_movie_type': {
                                                                        '$max': '$movie_type_id'
                                                                    }
                                                                }
                                                            }, {
                                                                '$project': {
                                                                    'proximo_movie_type': {
                                                                        '$sum': [
                                                                            '$proximo_movie_type', 1
                                                                        ]
                                                                    }, 
                                                                    '_id': 0
                                                                }
                                                            }
                                                        ])
                    

                    proximo_movie_type_list = list(proximo_movie_type)

                

                    if proximo_movie_type_list:
                        proximo_movie_type = int(proximo_movie_type_list[0]['proximo_movie_type'])
                    else:
                        proximo_movie_type = 1  
            
                
                
                    self.mongo.db["movies_type"].insert_one({"movie_type_id": proximo_movie_type , "movie_type_name": movie_type})
                
                    df_movie_type = self.recupera_movie_typeByName(movie_type)
                    

                

                    novo_movie_type = MovieType(df_movie_type.movie_type_id.values[0],df_movie_type.movie_type_name.values[0])
                    print(novo_movie_type.to_string())
                    self.mongo.close()
            except ValueError:
                print("Valor inválido")
                return novo_movie_type
            else:
                self.mongo.close()
                print(f"O genero {movie_type} já está cadastrado.")
                return None
            

    def excluir_movie_type(self):
        try:
            self.mongo.connect()
            
            self.relatorio.get_relatorio_movies_type()
        
            codigo_movie_type = int(input("Código do genero de filme que irá excluir: "))        


            if not self.verifica_existencia_movie_type(codigo_movie_type):            
                df_movie_type = self.recupera_movie_typeByID(codigo_movie_type)
        

                opcao_excluir = input(f"Tem certeza que deseja excluir o genero de código {codigo_movie_type} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    print("Atenção, ao campo ( genero da tabela filmes será atualizado também ) deseja continuar?")
                    opcao_excluir = input(f"Tem certeza que deseja excluir o genero de código {codigo_movie_type} [S ou N]: ")
                    if opcao_excluir.lower() == "s":
                        self.mongo.db["movies_type"].delete_one({"movie_type_id": codigo_movie_type})
                        self.mongo.db["movies"].update_many({"movie_type_id": f"{codigo_movie_type}"}, {"$set": {"movie_type_id": "null", "movie_genero": "null"}})
                        movie_type_excluido = MovieType(df_movie_type.movie_type_id.values[0],df_movie_type.movie_type_name.values[0])
                        self.mongo.close()
                        print("Genero Removido com Sucesso!")
                        print(movie_type_excluido.to_string())
            else:
                self.mongo.close()
                print(f"O código {codigo_movie_type} não existe.")
        except ValueError:
            print("Valor inválido")

    def recupera_movie_typeByID(self, movie_type:int=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_movie_type = pd.DataFrame(list(self.mongo.db["movies_type"].find({"movie_type_id": movie_type}, {"movie_type_id": 1,"movie_type_name": 1, "_id": 0})))
        
        if external:
            self.mongo.close()

        return df_movie_type
    
    def recupera_movie_typeByName(self, movie_type:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_movie_type = pd.DataFrame(list(self.mongo.db["movies_type"].find({"movie_type_name": f"{movie_type}"}, {"movie_type_id": 1,"movie_type_name": 1, "_id": 0})))
        
        if external:
            self.mongo.close()

        return df_movie_type

    def verifica_existencia_movie_type(self, movie_type_id:int=None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_movie_type = pd.DataFrame(self.mongo.db["movies_type"].find({"movie_type_id": movie_type_id}, {"movie_type_id": 1,"movie_type_name": 1,"_id": 0}))

        if external:
            self.mongo.close()

        return df_movie_type.empty
    
    def recupera_movie(self, movie_type_id:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_movie = pd.DataFrame(self.mongo.db["movies"].find({"movie_type_id":f"{movie_type_id}"}, {"movie_id": 1, "movie_type_id": 1, "movie_genero": 1, "movie_name": 1, "movie_description": 1, "movie_priece": 1, "_id": 0}))
        
        if external:
            self.mongo.close()

        return df_movie
