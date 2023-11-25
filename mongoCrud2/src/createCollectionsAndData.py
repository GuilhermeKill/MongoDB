import logging
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries
import json

LIST_OF_COLLECTIONS = ["users", "movies", "user_movie", "movies_type"]
logger = logging.getLogger(name="Example_CRUD_MongoDB")
logger.setLevel(level=logging.WARNING)
mongo = MongoQueries()

def createCollections(drop_if_exists:bool=False):
    """
        Lista as coleções existentes, verificar se as coleções padrão estão entre as coleções existentes.
        Caso exista e o parâmetro de exclusão esteja configurado como True, irá apagar a coleção e criar novamente.
        Caso não exista, cria a coleção.
        
        Parameter:
                  - drop_if_exists: True  -> apaga a tabela existente e recria
                                    False -> não faz nada
    """
    mongo.connect()
    existing_collections = mongo.db.list_collection_names()
    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} droped!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} created!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")
    mongo.close()

    mongo.connect()
    mongo.db["users"].insert_many([{"user_id": 1, "cpf": "65845154", "user_fullname": "Guilherme", "telephone": "351684874", "email": "Guilherme@gmail.com"},
                                {"user_id": 2, "cpf": "6541551845154", "user_fullname": "Ludovico", "telephone": "81588554874", "email": "Ludovico@gmail.com"}])

    mongo.db["movies_type"].insert_many([{"movie_type_id": 1, "movie_type_name": "terror"},
                                        {"movie_type_id": 2, "movie_type_name": "romance"}])

    mongo.db["movies"].insert_many([{"movie_id": 1, "movie_name": "A freira", "movie_type_id": "1", "movie_genero": "terror", "movie_description": "ótimo filme", "movie_priece": 100},
                                {"movie_id": 2, "movie_name": "vOcê e eu", "movie_type_id": "2", "movie_genero": "romance", "movie_description": "filme para amar", "movie_priece": 400}])


    mongo.db["user_movie"].insert_many([{"user_movie_id": 1, "movie_id": 1, "user_id": 2},
                                        {"user_movie_id": 2, "movie_id": 2, "user_id": 1}])


    mongo.close()


def insert_many(data:json, collection:str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()

if __name__ == "__main__":
    logging.warning("Starting")
    createCollections(drop_if_exists=True)
    logging.warning("End")