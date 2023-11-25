import pandas as pd
from model.users import User
from reports.relatorios import Relatorio
from conexion.mongo_queries import MongoQueries

class Controller_User:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_user(self) -> User:
        try:
            self.mongo.connect()

            # Solicita ao usuario o novo CPF
            cpf = input("CPF (Novo): ")

            if self.verifica_existencia_user(cpf):
                proximo_user = self.mongo.db["users"].aggregate([
                                                        {
                                                            '$group': {
                                                                '_id': '$users', 
                                                                'proximo_user': {
                                                                    '$max': '$user_id'
                                                                }
                                                            }
                                                        }, {
                                                            '$project': {
                                                                'proximo_user': {
                                                                    '$sum': [
                                                                        '$proximo_user', 1
                                                                    ]
                                                                }, 
                                                                '_id': 0
                                                            }
                                                        }
                                                    ])
                

                proximo_user_list = list(proximo_user)

                # Verifica se a lista não está vazia antes de tentar acessar o primeiro elemento
                if proximo_user_list:
                    proximo_user = int(proximo_user_list[0]['proximo_user'])
                else:
                    # Trata o caso em que a lista está vazia (nenhum documento retornado)
                    proximo_user = 1  # ou qualquer valor padrão desejado
        
                user_fullname = input("Nome (Novo): ")
                telephone = input("Telefone (Novo): ")
                email = input("Email (Novo): ")
            
                self.mongo.db["users"].insert_one({"user_id": proximo_user ,"cpf": cpf, "user_fullname": user_fullname, "telephone": telephone, "email": email})
            
                df_user = self.recupera_user(cpf)


                print(df_user.to_string())

                novo_user = User(df_user.user_id.values[0],df_user.cpf.values[0], df_user.user_fullname.values[0], df_user.telephone.values[0], df_user.email.values[0])
                # Exibe os atributos do novo user
                print(novo_user.to_string())
                self.mongo.close()
            
                return novo_user
            else:
                self.mongo.close()
                print(f"O CPF {cpf} já está cadastrado.")
                return None
        except ValueError:
            print("Valor inválido") 

    def atualizar_user(self) -> User:
        try:
            self.mongo.connect()
            self.relatorio.get_relatorio_users()
        
            cpf = input("CPF do user que deseja alterar: ")

            if not self.verifica_existencia_user(cpf):
                novo_cpf = input("CPF (Novo): ")
                novo_user_fullname = input("Nome (Novo): ")
                novo_telephone = input("Telephone (Novo): ")
                novo_email = input("Email (Novo): ")
                self.mongo.db["users"].update_one({"cpf": f"{cpf}"}, {"$set": {"cpf": novo_cpf, "user_fullname": novo_user_fullname, "telephone": novo_telephone, "email": novo_email}})
                df_user = self.recupera_user(novo_cpf)

                print(df_user.to_string())

                user_atualizado = User(df_user.user_id.values[0],df_user.cpf.values[0], df_user.user_fullname.values[0], df_user.telephone.values[0], df_user.email.values[0])
                print(user_atualizado.to_string())
                self.mongo.close()
                return user_atualizado
            else:
                self.mongo.close()
                print(f"O CPF {cpf} não existe.")
                return None
        except ValueError:
            print("Valor inválido") 


    def recupera_user(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_user = pd.DataFrame(list(self.mongo.db["users"].find({"cpf":f"{cpf}"}, {"user_id": 1,"cpf": 1, "user_fullname": 1, "telephone": 1, "email": 1, "_id": 0})))
        
        if external:
            self.mongo.close()

        return df_user

    def verifica_existencia_user(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_user = pd.DataFrame(self.mongo.db["users"].find({"cpf":f"{cpf}"}, {"cpf": 1, "user_fullname": 1, "telephone": 1, "email": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_user.empty
    
   