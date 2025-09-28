import dropbox
import pandas as pd
from io import BytesIO
import dataframe_image as dfi
import streamlit as st
import matplotlib.pyplot as plt


class TabelaBase:
    colunas = []

    def __init__(self, caminho_dropbox, dbx):
        self.caminho_dropbox = caminho_dropbox
        self.dbx = dbx

    def baixar(self, caminho, nome_planilha):
        """Baixa o arquivo do Dropbox e carrega como Dataframe"""

        _, res = self.dbx.files_download(caminho)

        

        df = pd.read_excel(BytesIO(res.content), dtype=str,  header=4, index_col=None, usecols=["NOME", "COMISSÁRIO", "CERT", "FOTO", " ROUPA "], sheet_name=nome_planilha)
        df = df.fillna("")

        

        return df

        

        
    

    def salvar(self, df):
        """Salva o Dataframe atualizado no Dropbox"""

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        self.dbx.files_upload(output.read(), self.caminho_dropbox, mode=dropbox.files.WriteMode.overwrite)

        print(f"Arquivo {self.caminho_dropbox} atualizado com sucesso!")


    
    def inserir(self, nova_linha: dict):
        """Insere dados na tabela"""

        df = self.baixar()

        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)

        self.salvar(df)

    
    def listar_tabela(self):
        """Lista todas as linhas da tabela em formato de dicionario"""

        df = self.baixar()
        return df.to_dict(orient="records")
    
    
    def listar_pastas(self):
        """Lista todas as pastas e arquivos no caminho informado"""
        try:
            result = self.dbx.files_list_folder(self.caminho_dropbox)

            for entry in result.entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    print(f'[PASTA]  {entry.path_display}')
                
                elif isinstance(entry, dropbox.files.FileMetadata):
                    print(f'[ARQUIVO]  {entry.path_display}')

        except Exception as e:
            print("Erro ao listar:", e)


    def gerador_de_caminho(self, data):

        MESES_PT = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }
        ano, mes, dia = str(data).split('-')
        caminho_base = '/RESERVAS'
        nome_mes = MESES_PT[int(mes)].upper()
        caminho_data = f'{mes} {nome_mes} {ano}'

        caminho_final = f"{caminho_base}/{ano}/{caminho_data}/{caminho_data}.xlsx"
        nome_planilha = f'{dia}(MANHÃ)'

        return(caminho_final, nome_planilha)
    
    def salvar_tabela_como_imagem(self, df, filename="planilha.png"):
        fig, ax = plt.subplots(figsize=(len(df.columns) * 2, len(df) * 0.5 + 2))

        ax.axis('off')  # tira os eixos
        tabela = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        loc='center')
        tabela.auto_set_font_size(False)
        tabela.set_fontsize(10)
        
        # 👉 Ajusta automaticamente a largura de todas as colunas
        tabela.auto_set_column_width(col=list(range(len(df.columns))))
        
        tabela.scale(1.2, 1.2)  # aumenta tamanho
        plt.savefig(filename, bbox_inches="tight", dpi=150)
        plt.close(fig)
        
        return filename
    

    def df_para_html_selecionadas(self, df):
        """
        Recebe um DataFrame e uma lista de colunas a exibir.
        Retorna uma tabela HTML estilizada.
        """
        # Seleciona apenas as colunas desejadas

        # Início da tabela
        html = '<table style="border-collapse: collapse; width: 100%;">'

        # Cabeçalho
        html += '<tr>'
        for col in df.columns:
            html += f'<th style="border: 1px solid black; padding: 6px; background-color: #f2f2f2; text-align: center">{col}</th>'
        html += '</tr>'

        # Linhas
        for _, row in df.iterrows():
            html += '<tr>'
            for val in row:
                html += f'<td style="border: 1px solid black; padding: 6px; text-align: center; font-size: 16px; height: 30px;">{val}</td>'
            html += '</tr>'


        html += '</table>'
        return html