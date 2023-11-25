# Exemplo de Sistema em Python fazendo CRUD no MongoDB

Esse sistema de exemplo é composto por um conjunto de coleções(collections) que representam pedidos de vendas, contendo coleções como: clientes, fornecedores, produtos, pedidos e itens de pedido.

O sistema exige que as coleções existam, então basta executar o script Python a seguir para criação das coleções e preenchimento de dados de exemplos:
```shell
~$ python createCollectionsAndData.py
```
Para executar o sistema basta executar o script Python a seguir:
```shell
~$ python principal.py
```

## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/DIAGRAMA_RELACIONAL_PEDIDOS.pdf) (lógico) do sistema e o relatório de atividades do grupo.
    * O sistema possui cinco entidades: users, movies. movies_type, user_movie
- [src](src): Nesse diretório estão os scripts do sistema
    * [conexion](src/conexion): Nesse repositório encontra-se o [módulo de conexão com o banco de dados Mongo](src/conexion/mongo_queries.py). Esse módulo possui algumas funcionalidades úteis para execução de instruções. O módulo do Mongo apenas realiza a conexão, os métodos CRUD e de recuperação de dados são implementados diretamente nos objetos controladores (_Controllers_) e no objeto de Relatório (_reports_).

      - Exemplo de criação de um documento no Mongo:
      ```python
            from conexion.mongo_queries import MongoQueries
            import pandas as pd
            # Cria o objeto MongoQueries
            mongo = MongoQueries()

            # Realiza a conexão com o Mongo
            mongo.connect()

            # Solicita ao usuario o novo CPF
            cpf = input("CPF (Novo): ")
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Insere e persiste o novo cliente
            mongo.db["clientes"].insert_one({"cpf": cpf, "nome": nome})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = pd.DataFrame(list(mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0})))
            # Exibe os dados do cliente em formato DataFrame
            print(df_cliente)

            # Fecha a conexão com o Mong
            mongo.close()
      ```
    * [controller](src/controller/): Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.
    * [model](src/model/): Nesse diretório encontram-ser as classes das entidades descritas no [diagrama relacional](diagrams/DIAGRAMA_RELACIONAL_PEDIDOS.pdf)
    * [reports](src/reports/) Nesse diretório encontra-se a [classe](src/reports/relatorios.py) responsável por gerar todos os relatórios do sistema
    * [utils](src/utils/): Nesse diretório encontram-se scripts de [configuração](src/utils/config.py) e automatização da [tela de informações iniciais](src/utils/splash_screen.py)
    * [createCollectionsAndData.py](src/createCollectionsAndData.py): Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script [principal.py](src/principal.py) para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em alguma outra IDE de acesso ao Banco de Dados.
    * [principal.py](src/principal.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`

## Contato
- [LinkedIn](https://www.linkedin.com/in/grkill)