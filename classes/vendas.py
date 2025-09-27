from classes.base import TabelaBase


class VendasTabela(TabelaBase):
    colunas = ["Nome", "cpf", "vendedor", "valor"]

    def buscar_por_nome(self, nome:str):
        df = self.baixar()

        return df[df['Nome'].str.contains(nome, case=False, na=False)].to_dict(orient='records')
    
    def inserir(self, nome, cpf, vendedor, valor):

        nova_linha = {
            "Nome":nome,
            "cpf":cpf,
            "vendedor":vendedor,
            "valor":valor
        }
        return super().inserir(nova_linha)