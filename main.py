import locale
from classes.base import TabelaBase
import streamlit as st
from datetime import datetime
from functions.dropbox_connection import dropbox_connection


st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

dbx = dropbox_connection()



base = TabelaBase('', dbx)

st.title('Planilhas')
data = st.date_input('Insira a data da planilha', format='DD/MM/YYYY')

if st.button('Pesquisar'):

    caminho, nome_planilha = base.gerador_de_caminho(data)
    df = base.baixar(caminho, nome_planilha)
    
    

    # colunas = ["B", "D", "E", "F", "H"]  # Colunas que quer exibir
    # st.markdown(base.df_para_html_selecionadas(df), unsafe_allow_html=True)
    st.image(df, width="stretch")
    


