import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import os
import numpy as np
from datetime import datetime
import mysql.connector
from utils.queries import *
from utils.user import *
# from workalendar.america import Brazil
# import openpyxl

def handle_login(userName, userPassoword):
    users = st.secrets["users"]

    if userName not in users['emails']:
        st.error("Usuário sem permissão.")
        return
    
    if user_data := login(userName, userPassoword):
        st.session_state["loggedIn"] = True
        st.session_state["user_data"] = user_data
    else:
        st.session_state["loggedIn"] = False
        st.error("Email ou senha inválidos!")

def show_login_page():
    st.markdown(""" 
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
                }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4,1])
    col1.write("## DashBoard")
    userName = st.text_input(label="", value="", placeholder="Login", label_visibility="collapsed")
    userPassword = st.text_input(label="", value="", placeholder="Senha",type="password", label_visibility="collapsed")
    st.button("login", on_click=handle_login, args=(userName, userPassword))

LOGGER = get_logger(__name__)

def mysql_connection_fb():
  mysql_config = st.secrets["mysql_fb"]

  conn_fb = mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database'],
        user=mysql_config['username'],
        password=mysql_config['password']
    )    
  return conn_fb


def execute_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)

    # Obter nomes das colunas
    column_names = [col[0] for col in cursor.description]
  
    # Obter resultados
    result = cursor.fetchall()
  
    cursor.close()
    return result, column_names

def run():

    ######## Puxando Dados #########
    conn_fb = mysql_connection_fb()

    def casas():
        result, column_names = execute_query(GET_CASAS, conn_fb)
        df_casas = pd.DataFrame(result, columns=column_names)   

        return df_casas
    df_casas = casas()

    def extrato_zig():
        result, column_names = execute_query(GET_EXTRATO_ZIG, conn_fb)
        df_extrato_zig = pd.DataFrame(result, columns=column_names)   

        df_extrato_zig['Data_Liquidacao'] = pd.to_datetime(df_extrato_zig['Data_Liquidacao']) 
        df_extrato_zig['Data_Transacao'] = pd.to_datetime(df_extrato_zig['Data_Transacao']) 

        return df_extrato_zig
    df_extrato_zig = extrato_zig()

    def zig_faturamento():
        result, column_names = execute_query(GET_ZIG_FATURAMENTO, conn_fb)
        df_zig_faturam = pd.DataFrame(result, columns=column_names)   

        df_zig_faturam['Data_Venda'] = pd.to_datetime(df_zig_faturam['Data_Venda']) 

        return df_zig_faturam
    df_zig_faturam = zig_faturamento()    

    def parcelas_receit_extr():
        result, column_names = execute_query(GET_PARCELAS_RECEITAS_EXTRAORDINARIAS, conn_fb)
        df_parc_receit_extr = pd.DataFrame(result, columns=column_names)   

        df_parc_receit_extr['Data_Ocorrencia'] = pd.to_datetime(df_parc_receit_extr['Data_Ocorrencia']) 
        df_parc_receit_extr['Vencimento_Parcela'] = pd.to_datetime(df_parc_receit_extr['Vencimento_Parcela'])
        df_parc_receit_extr['Recebimento_Parcela'] = pd.to_datetime(df_parc_receit_extr['Recebimento_Parcela'])

        return df_parc_receit_extr
    df_parc_receit_extr = parcelas_receit_extr()    

    def custos_blueme_sem_parcelam():
        result, column_names = execute_query(GET_CUSTOS_BLUEME_SEM_PARCELAMENTO, conn_fb)
        df_custos_blueme_sem_parcelam = pd.DataFrame(result, columns=column_names)   

        df_custos_blueme_sem_parcelam['Data_Vencimento'] = pd.to_datetime(df_custos_blueme_sem_parcelam['Data_Vencimento'], errors='coerce') 
        df_custos_blueme_sem_parcelam['Previsao_Pgto'] = pd.to_datetime(df_custos_blueme_sem_parcelam['Previsao_Pgto'], errors='coerce') 
        df_custos_blueme_sem_parcelam['Realizacao_Pgto'] = pd.to_datetime(df_custos_blueme_sem_parcelam['Realizacao_Pgto'], errors='coerce') 
        df_custos_blueme_sem_parcelam['Data_Competencia'] = pd.to_datetime(df_custos_blueme_sem_parcelam['Data_Competencia'], errors='coerce') 
        df_custos_blueme_sem_parcelam['Data_Lancamento'] = pd.to_datetime(df_custos_blueme_sem_parcelam['Data_Lancamento'], errors='coerce') 

        return df_custos_blueme_sem_parcelam
    df_custos_blueme_sem_parcelam = custos_blueme_sem_parcelam()  

    def custos_blueme_com_parcelam():
        result, column_names = execute_query(GET_CUSTOS_BLUEME_COM_PARCELAMENTO, conn_fb)
        df_custos_blueme_com_parcelam = pd.DataFrame(result, columns=column_names)   

        df_custos_blueme_com_parcelam['Vencimento_Parcela'] = pd.to_datetime(df_custos_blueme_com_parcelam['Vencimento_Parcela'], errors='coerce') 
        df_custos_blueme_com_parcelam['Previsao_Parcela'] = pd.to_datetime(df_custos_blueme_com_parcelam['Previsao_Parcela'], errors='coerce') 
        df_custos_blueme_com_parcelam['Realiz_Parcela'] = pd.to_datetime(df_custos_blueme_com_parcelam['Realiz_Parcela'], errors='coerce') 
        df_custos_blueme_com_parcelam['Data_Lancamento'] = pd.to_datetime(df_custos_blueme_com_parcelam['Data_Lancamento'], errors='coerce') 

        return df_custos_blueme_com_parcelam
    df_custos_blueme_com_parcelam = custos_blueme_com_parcelam()
    
    def extratos_bancarios():
        result, column_names = execute_query(GET_EXTRATOS_BANCARIOS, conn_fb)
        df_extratos_bancarios = pd.DataFrame(result, columns=column_names)   

        df_extratos_bancarios['Data_Transacao'] = pd.to_datetime(df_extratos_bancarios['Data_Transacao'], errors='coerce')

        return df_extratos_bancarios
    df_extratos_bancarios = extratos_bancarios()     

    def mutuos():
        result, column_names = execute_query(GET_MUTUOS, conn_fb)
        df_mutuos = pd.DataFrame(result, columns=column_names)   

        df_mutuos['Data_Mutuo'] = pd.to_datetime(df_mutuos['Data_Mutuo'], errors='coerce') 

        return df_mutuos
    df_mutuos = mutuos()         

    def tesouraria():
        result, column_names = execute_query(GET_TESOURARIA, conn_fb)
        df_tesouraria = pd.DataFrame(result, columns=column_names)   

        df_tesouraria['Data_Transacao'] = pd.to_datetime(df_tesouraria['Data_Transacao'], errors='coerce') 

        return df_tesouraria
    df_tesouraria = tesouraria()      

    def ajustes_conciliacao():
        result, column_names = execute_query(GET_AJUSTES_CONCILIACAO, conn_fb)
        df_ajustes_conciliacao = pd.DataFrame(result, columns=column_names)   

        df_ajustes_conciliacao['Data_Ajuste'] = pd.to_datetime(df_ajustes_conciliacao['Data_Ajuste'], errors='coerce') 

        return df_ajustes_conciliacao
    df_ajustes_conciliacao = ajustes_conciliacao()         

    ######## Definindo Relatorio ########
    st.write("# Conciliacao FB")

    st.markdown(
        """
        Utilize as abas localizadas no lado esquerdo para buscar suas análises.
    """
    ) 

    if "df_casas" not in st.session_state:
        st.session_state["df_casas"] = df_casas

    if "df_extrato_zig" not in st.session_state:
        st.session_state["df_extrato_zig"] = df_extrato_zig

    if "df_zig_faturam" not in st.session_state:
        st.session_state["df_zig_faturam"] = df_zig_faturam

    if "df_parc_receit_extr" not in st.session_state:
        st.session_state["df_parc_receit_extr"] = df_parc_receit_extr

    if "df_custos_blueme_sem_parcelam" not in st.session_state:
        st.session_state["df_custos_blueme_sem_parcelam"] = df_custos_blueme_sem_parcelam

    if "df_custos_blueme_com_parcelam" not in st.session_state:
        st.session_state["df_custos_blueme_com_parcelam"] = df_custos_blueme_com_parcelam

    if "df_extratos_bancarios" not in st.session_state:
        st.session_state["df_extratos_bancarios"] = df_extratos_bancarios

    if "df_mutuos" not in st.session_state:
        st.session_state["df_mutuos"] = df_mutuos

    if "df_tesouraria" not in st.session_state:
        st.session_state["df_tesouraria"] = df_tesouraria  

    if "df_ajustes_conciliacao" not in st.session_state:
        st.session_state["df_ajustes_conciliacao"] = df_ajustes_conciliacao                                                        

if __name__ == "__main__":
     ######## Config Pag ##########
    st.set_page_config(
    page_title="Conciliacao_FB",
    page_icon="💰",
    )
    
    with st.sidebar:
        st.button(label="Logout", on_click=logout)

    if "loggedIn" not in st.session_state:
        st.session_state["loggedIn"] = False
        st.session_state["user_date"] = None

    if not st.session_state["loggedIn"]:
        show_login_page()
        st.stop()
    else:
        run()


