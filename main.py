import locale
from classes.base import TabelaBase
import streamlit as st
from datetime import datetime
from functions.dropbox_connection import dropbox_connection



dbx = dropbox_connection()



base = TabelaBase('', dbx)

st.title('Planilhas')
data = st.date_input('Insira a data da planilha', format='DD/MM/YYYY')

if st.button('Pesquisar'):

    caminho, nome_planilha = base.gerador_de_caminho(data)
    st.table(base.baixar(caminho, nome_planilha))
    set= True


