from utils import config

class SplashScreen:

    def __init__(self):
        self.created_by = "Henrique Schuraiber, Guilherme Reis KIll,"
        self.created_by1 = "Rodrigo Kill Correa, Ana Carolina Lopes Dalvi,"
        self.created_by2 = "Ludovico Monjardim, Kevin Dos Reis Hartwig"

        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2022/2"

    def get_documents_count(self, collection_name):
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE VENDAS                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - Usuarios:            {str(self.get_documents_count(collection_name="users")).rjust(5)}
        #      2 - Filmes:              {str(self.get_documents_count(collection_name="movies")).rjust(5)}
        #      3 - Genero de filmes:    {str(self.get_documents_count(collection_name="movies_type")).rjust(5)}
        #      4 - Vendas:              {str(self.get_documents_count(collection_name="user_movie")).rjust(5)}
        #      
        #
        #  CRIADO POR: {self.created_by}
                       {self.created_by1}
        #              {self.created_by2}
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """