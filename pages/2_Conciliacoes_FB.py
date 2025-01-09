import streamlit as st
import pandas as pd
import datetime
import calendar
from utils.functions.general_functions import *
from utils.queries import *
from workalendar.america import Brazil

st.set_page_config(
    page_title="Conciliacao_FB",
    page_icon="💰",
    layout="wide"
)


# Adicionando o checkbox para desativar o filtro de datas
able_date_filter = st.checkbox("Filtrar datas")

# Filtrando Data
today = datetime.datetime.now()
last_year = today.year - 1
jan_last_year = datetime.datetime(last_year, 1, 1)
jan_this_year = datetime.datetime(today.year, 1, 1)
last_day_of_month = calendar.monthrange(today.year, today.month)[1]
this_month_this_year = datetime.datetime(today.year, today.month, last_day_of_month)
dec_this_year = datetime.datetime(today.year, 12, 31)

## 5 meses atras
month_sub_3 = today.month - 3
year = today.year

if month_sub_3 <= 0:
    # Se o mês resultante for menor ou igual a 0, ajustamos o ano e corrigimos o mês
    month_sub_3 += 12
    year -= 1

start_of_three_months_ago = datetime.datetime(year, month_sub_3, 1)


date_input = st.date_input("Período",
                           (jan_this_year, this_month_this_year),
                           min_value=jan_last_year,
                           max_value=dec_this_year,
                           format="DD/MM/YYYY"
                           )

# Convertendo as datas do "date_input" para datetime
start_date = pd.to_datetime(date_input[0])
end_date = pd.to_datetime(date_input[1])


# Filtrando casas
df_casas = st.session_state["df_casas"]
casas = df_casas['Casa'].tolist()
casa = st.selectbox("Casa", casas)

# Definindo um dicionário para mapear nomes de casas a IDs de casas
mapeamento_lojas = dict(zip(df_casas["Casa"], df_casas["ID_Casa"]))

# Obtendo o ID da casa selecionada
id_casa = mapeamento_lojas[casa]
st.write('ID da casa selecionada:', id_casa)

st.divider()

### Definindo Bases ###

## Extratos Zig
st.subheader("Extrato Zig")
df_extrato_zig = st.session_state["df_extrato_zig"]
df_extrato_zig_filtrada = df_extrato_zig[df_extrato_zig['ID_Casa'] == id_casa]
if able_date_filter:
    df_extrato_zig_filtrada = df_extrato_zig_filtrada[(df_extrato_zig_filtrada["Data_Liquidacao"] >= start_date) & (df_extrato_zig_filtrada["Data_Liquidacao"] <= end_date)]
else:    
    df_extrato_zig_filtrada = df_extrato_zig_filtrada

st.dataframe(df_extrato_zig_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Zig_Faturamento
st.subheader("Zig Faturamento")
df_zig_faturam = st.session_state["df_zig_faturam"]
df_zig_faturam_filtrada = df_zig_faturam[df_zig_faturam['ID_Casa'] == id_casa]
if able_date_filter:
    df_zig_faturam_filtrada = df_zig_faturam_filtrada[(df_zig_faturam_filtrada["Data_Venda"] >= start_date) & (df_zig_faturam_filtrada["Data_Venda"] <= end_date)]
else:    
    df_zig_faturam_filtrada = df_zig_faturam_filtrada

st.dataframe(df_zig_faturam_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Parcelas Receitas Extraordinarias
st.subheader("Parcelas Receitas Extraordinarias")
df_parc_receit_extr = st.session_state["df_parc_receit_extr"]
df_parc_receit_extr_filtrada = df_parc_receit_extr[df_parc_receit_extr['ID_Casa'] == id_casa]
if able_date_filter:
    df_parc_receit_extr_filtrada = df_parc_receit_extr_filtrada[(df_parc_receit_extr_filtrada["Recebimento_Parcela"] >= start_date) & (df_parc_receit_extr_filtrada["Recebimento_Parcela"] <= end_date)]
else:
    df_parc_receit_extr_filtrada = df_parc_receit_extr_filtrada

st.dataframe(df_parc_receit_extr_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Custos BlueMe Sem Parcelamento
st.subheader("Despesas BlueMe Sem Parcelamento")
df_custos_blueme_sem_parcelam = st.session_state["df_custos_blueme_sem_parcelam"]
df_custos_blueme_sem_parcelam_filtrada = df_custos_blueme_sem_parcelam[df_custos_blueme_sem_parcelam['ID_Casa'] == id_casa]
if able_date_filter:
    df_custos_blueme_sem_parcelam_filtrada = df_custos_blueme_sem_parcelam_filtrada[(df_custos_blueme_sem_parcelam_filtrada["Realizacao_Pgto"] >= start_date) & (df_custos_blueme_sem_parcelam_filtrada["Realizacao_Pgto"] <= end_date)]
else:    
    df_custos_blueme_sem_parcelam_filtrada = df_custos_blueme_sem_parcelam_filtrada

st.dataframe(df_custos_blueme_sem_parcelam_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Custos BlueMe Com Parcelamento
st.subheader("Despesas BlueMe Com Parcelamento")
df_custos_blueme_com_parcelam = st.session_state["df_custos_blueme_com_parcelam"]
df_custos_blueme_com_parcelam_filtrada = df_custos_blueme_com_parcelam[df_custos_blueme_com_parcelam['ID_Casa'] == id_casa]
if able_date_filter:
    df_custos_blueme_com_parcelam_filtrada = df_custos_blueme_com_parcelam_filtrada[(df_custos_blueme_com_parcelam_filtrada["Realiz_Parcela"] >= start_date) & (df_custos_blueme_com_parcelam_filtrada["Realiz_Parcela"] <= end_date)] 
else:
    df_custos_blueme_com_parcelam_filtrada = df_custos_blueme_com_parcelam_filtrada
st.dataframe(df_custos_blueme_com_parcelam_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Extratos Bancarios
st.subheader("Extratos Bancarios")
df_extratos_bancarios = st.session_state["df_extratos_bancarios"]
df_extratos_bancarios_filtrada = df_extratos_bancarios[df_extratos_bancarios['ID_Casa'] == id_casa]
if able_date_filter:
    df_extratos_bancarios_filtrada = df_extratos_bancarios_filtrada[(df_extratos_bancarios_filtrada["Data_Transacao"] >= start_date) & (df_extratos_bancarios_filtrada["Data_Transacao"] <= end_date)] 
else:
    df_extratos_bancarios_filtrada = df_extratos_bancarios_filtrada
st.dataframe(df_extratos_bancarios_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Mutuos
st.subheader("Mutuos")

df_mutuos = st.session_state["df_mutuos"]
df_mutuos_filtrada = df_mutuos[(df_mutuos['ID_Casa_Saida'] == id_casa) | (df_mutuos['ID_Casa_Entrada'] == id_casa)] 
if able_date_filter:
    df_mutuos_filtrada = df_mutuos_filtrada[(df_mutuos["Data_Mutuo"] >= start_date) & (df_mutuos_filtrada["Data_Mutuo"] <= end_date)] 
else:
    df_mutuos_filtrada = df_mutuos_filtrada
st.dataframe(df_mutuos_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Tesouraria
st.subheader("Tesouraria")

df_tesouraria = st.session_state["df_tesouraria"]
df_tesouraria_filtrada = df_tesouraria[df_tesouraria['ID_Casa'] == id_casa]
if able_date_filter:
    df_tesouraria_filtrada = df_tesouraria_filtrada[(df_tesouraria_filtrada["Data_Transacao"] >= start_date) & (df_tesouraria_filtrada["Data_Transacao"] <= end_date)] 
else:
    df_tesouraria_filtrada = df_tesouraria_filtrada
st.dataframe(df_tesouraria_filtrada, use_container_width=True, hide_index=True)

st.divider()

## Ajustes Conciliação
st.subheader("Ajustes Conciliação")

df_ajustes_conciliacao = st.session_state["df_ajustes_conciliacao"]
df_ajustes_conciliacao_filtrada = df_ajustes_conciliacao[df_ajustes_conciliacao['ID_Casa'] == id_casa]
if able_date_filter:
    df_ajustes_conciliacao_filtrada = df_ajustes_conciliacao_filtrada[(df_ajustes_conciliacao_filtrada["Data_Ajuste"] >= start_date) & (df_ajustes_conciliacao_filtrada["Data_Ajuste"] <= end_date)] 
else:
    df_ajustes_conciliacao_filtrada = df_ajustes_conciliacao_filtrada
st.dataframe(df_ajustes_conciliacao_filtrada, use_container_width=True, hide_index=True)

st.divider()


## Exportando em Excel

excel_filename = 'Conciliacao_FB.xlsx'

if st.button('Atualizar Planilha Excel'):
  sheet_name_zig = 'df_extrato_zig'
  export_to_excel(df_extrato_zig_filtrada, sheet_name_zig, excel_filename)

  sheet_name_zig = 'df_zig_faturam'
  export_to_excel(df_zig_faturam_filtrada, sheet_name_zig, excel_filename)  

  sheet_name_view_parc_agrup = 'view_parc_agrup'
  export_to_excel(df_parc_receit_extr_filtrada, sheet_name_view_parc_agrup, excel_filename)

  sheet_name_custos_blueme_sem_parcelamento = 'df_blueme_sem_parcelamento'
  export_to_excel(df_custos_blueme_sem_parcelam_filtrada, sheet_name_custos_blueme_sem_parcelamento, excel_filename)

  sheet_name_custos_blueme_com_parcelamento = 'df_blueme_com_parcelamento'
  export_to_excel(df_custos_blueme_com_parcelam_filtrada, sheet_name_custos_blueme_com_parcelamento, excel_filename)

  sheet_name_extratos = 'df_extratos'
  export_to_excel(df_extratos_bancarios_filtrada, sheet_name_extratos, excel_filename)

  df_mutuos_filtrada['Valor_Entrada'] = df_mutuos_filtrada.apply(lambda row: row['Valor'] if row['ID_Casa_Entrada'] == id_casa else 0, axis=1)
  df_mutuos_filtrada['Valor_Saida'] = df_mutuos_filtrada.apply(lambda row: row['Valor'] if row['ID_Casa_Saida'] == id_casa else 0, axis=1)
  df_mutuos_filtrada = df_mutuos_filtrada.drop('Valor', axis=1)
  sheet_name_mutuos = 'df_mutuos'
  export_to_excel(df_mutuos_filtrada, sheet_name_mutuos, excel_filename)

  sheet_name_tesouraria = 'df_tesouraria_trans'
  export_to_excel(df_tesouraria_filtrada, sheet_name_tesouraria, excel_filename)

  sheet_name_ajustes_conciliacao = 'df_ajustes_conciliaco'
  export_to_excel(df_ajustes_conciliacao_filtrada, sheet_name_ajustes_conciliacao, excel_filename)
  
  
  st.success('Arquivo atualizado com sucesso!')


if st.button('Baixar Excel'):
  if os.path.exists(excel_filename):
    with open(excel_filename, "rb") as file:
      file_content = file.read()
    st.download_button(
      label="Clique para baixar o arquivo Excel",
      data=file_content,
      file_name="Conciliacao_FB.xlsx",
      mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




