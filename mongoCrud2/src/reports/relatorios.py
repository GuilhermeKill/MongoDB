from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_users(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["users"].find({}, 
                                                     {"user_id": 1,
                                                      "movie_type_id": 1,
                                                      "user_fullname": 1,
                                                      "telephone": 1,
                                                      "cpf": 1,
                                                      "_id": 0
                                                     })
        df_movie_type = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_movie_type)        
        input("Pressione Enter para Sair do Relatório de usuarios")

    def get_relatorio_movies(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["movies"].find({}, 
                                                     {
                                                      "movie_id": 1,
                                                      "movie_name": 1,
                                                      "movie_description": 1,
                                                      "movie_priece": 1, 
                                                      "_id": 0
                                                     })
        df_movie = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_movie)        
        input("Pressione Enter para Sair do Relatório de filmes")

    def get_relatorio_movies_type(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["movies_type"].find({}, 
                                                     {
                                                      "movie_type_id": 1,
                                                      "movie_type_name": 1, 
                                                      "_id": 0
                                                     })
        df_movie_type = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_movie_type)        
        input("Pressione Enter para Sair do Relatório de generos")

    def get_relatorio_vendas(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db['user_movie'].aggregate([
    {
        '$lookup': {
            'from': 'users',
            'localField': 'user_id',
            'foreignField': 'user_id',
            'as': 'user_data'
        }
    },
    {
        '$unwind': {'path': '$user_data'}
    },
    {
        '$lookup': {
            'from': 'movies',
            'localField': 'movie_id',
            'foreignField': 'movie_id',
            'as': 'movie_data'
        }
    },
    {
        '$unwind': {'path': '$movie_data'}
    },
    {
        '$project': {
            '_id': 0,
            'naome': '$user_data.user_fullname',
            'preço do filme': '$movie_data.movie_priece'
        }
    }
])
        df_movie_type = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_movie_type)        
        input("\nPressione Enter para Sair do Relatório de vendas\n")






    def get_relatorio_quantia_gasta(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db['user_movie'].aggregate([
    {
        '$lookup': {
            'from': 'users',
            'localField': 'user_id',
            'foreignField': 'user_id',
            'as': 'user_data'
        }
    },
    {
        '$unwind': {
            "path": "$user_data"
        }
    },
    {
        '$lookup': {
            'from': 'movies',
            'localField': 'movie_id',
            'foreignField': 'movie_id',
            'as': 'movie_data'
        }
    },
    {
        '$unwind': {
            "path": "$movie_data"
        }
    },

    {
        '$group': {
            '_id': '$user_data.user_fullname',
            'total_movie_price': {
                '$sum': '$movie_data.movie_priece'
            }
        }
    },
    {
        '$project': {
            '_id': 0,
            'nome': '$_id',
            'gasto_total': '$total_movie_price'
        }
    }
])
        df_movie_type = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_movie_type)        
        input("\nPressione Enter para Sair do Relatório de vendas\n")




