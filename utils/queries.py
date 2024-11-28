

GET_CASAS = """
SELECT
te.ID as 'ID_Casa',
te.NOME_FANTASIA as 'Casa'
FROM T_EMPRESAS te
WHERE te.FK_GRUPO_EMPRESA = 100
ORDER BY te.NOME_FANTASIA 
"""

GET_EXTRATO_ZIG = """
SELECT 
tefz.ID as 'ID_Extrato',
te.ID as 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
tefz.DESCRICAO as 'Descricao',
tefz.DATA_LIQUIDACAO as 'Data_Liquidacao',
tefz.DATA_TRANSACAO as 'Data_Transacao',
tefz.VALOR as 'Valor'
FROM T_EXTRATO_FINANCEIRO_ZIG tefz 
INNER JOIN T_EMPRESAS te ON (tefz.ID_LOJA_ZIG = te.ID_ZIGPAY)
ORDER BY te.NOME_FANTASIA asc, tefz.ID DESC
"""


GET_PARCELAS_RECEITAS_EXTRAORDINARIAS = """
SELECT 
vpa.ID as 'ID_Receita',
te.ID as 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
trec.NOME as 'Cliente',
tre.DATA_OCORRENCIA as 'Data_Ocorrencia',
vpa.DATA_VENCIMENTO as 'Vencimento_Parcela',
vpa.DATA_RECEBIMENTO as 'Recebimento_Parcela',
vpa.VALOR_PARCELA as 'Valor_Parcela',
trec2.CONCAT_CATEGORIA_CLASSIFICACAO as 'Categoria_Class'
FROM View_Parcelas_Agrupadas vpa
INNER JOIN T_EMPRESAS te ON (vpa.FK_EMPRESA = te.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS tre ON (vpa.ID = tre.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS_CLIENTE trec ON (vpa.FK_CLIENTE = trec.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS_CLASSIFICACAO trec2 ON (tre.FK_CLASSIFICACAO = trec2.ID)
WHERE vpa.DATA_VENCIMENTO IS NOT NULL
ORDER BY vpa.DATA_RECEBIMENTO DESC
"""


GET_CUSTOS_BLUEME_SEM_PARCELAMENTO = """
SELECT 
tdr.ID as 'ID_Despesa',
te.ID as 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
tf.CORPORATE_NAME as 'Fornecedor_Razao_Social',
tdr.VALOR_LIQUIDO as 'Valor',
tdr.VENCIMENTO as 'Data_Vencimento',
tc.`DATA` as 'Previsao_Pgto',
tc2.`DATA` as 'Realizacao_Pgto',    
tdr.COMPETENCIA as 'Data_Competencia',
tdr.LANCAMENTO as 'Data_Lancamento',
tfdp.DESCRICAO as 'Forma_Pagamento',
tccg.DESCRICAO as 'Class_Cont_1',
tccg2.DESCRICAO as 'Class_Cont_2',
tscd.DESCRICAO as 'Status_Conf_Document',
tsad.DESCRICAO as 'Status_Aprov_Diret',
tsac.DESCRICAO as 'Status_Aprov_Caixa',
tsp.DESCRICAO as 'Status_Pgto',
tcb.NOME_DA_CONTA as 'Conta_Bancaria',
tdr.FK_LOJA_CNPJ as 'CNPJ_Loja'
FROM T_DESPESA_RAPIDA tdr
INNER JOIN T_EMPRESAS te ON (tdr.FK_LOJA = te.ID)
LEFT JOIN T_CONTAS_BANCARIAS tcb ON (tdr.FK_CONTA_BANCARIA = tcb.ID)
LEFT JOIN T_FORMAS_DE_PAGAMENTO tfdp ON (tdr.FK_FORMA_PAGAMENTO = tfdp.ID)
LEFT JOIN T_FORNECEDOR tf ON (tdr.FK_FORNECEDOR = tf.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 tccg ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = tccg.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 tccg2 ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = tccg2.ID)
LEFT JOIN T_STATUS_CONFERENCIA_DOCUMENTACAO tscd ON (tdr.FK_CONFERENCIA_DOCUMENTACAO = tscd.ID)
LEFT JOIN T_STATUS_APROVACAO_DIRETORIA tsad ON (tdr.FK_APROVACAO_DIRETORIA = tsad.ID)
LEFT JOIN T_STATUS_APROVACAO_CAIXA tsac ON (tdr.FK_APROVACAO_CAIXA = tsac.ID)
LEFT JOIN T_STATUS_PAGAMENTO tsp ON (tdr.FK_STATUS_PGTO = tsp.ID)
LEFT JOIN T_CALENDARIO tc ON (tdr.PREVISAO_PAGAMENTO = tc.ID)	
LEFT JOIN T_CALENDARIO tc2 ON (tdr.FK_DATA_REALIZACAO_PGTO = tc2.ID)
LEFT JOIN T_DEPESA_PARCELAS tdp ON (tdp.FK_DESPESA = tdr.ID)
WHERE 
    te.ID IS NOT NULL
    AND tdp.FK_DESPESA IS NULL
    AND (tdr.FK_DESPESA_TEKNISA IS NULL OR tdr.BIT_DESPESA_TEKNISA_PENDENTE = 1)
ORDER BY 
    tc2.`DATA` DESC
"""


GET_CUSTOS_BLUEME_COM_PARCELAMENTO = """
  SELECT
    tdp.ID as 'ID_Parcela',
    tdr.ID as 'ID_Despesa',
    te.NOME_FANTASIA as 'Casa',
    te.ID as 'ID_Casa',
    tdr.FK_LOJA_CNPJ as 'CNPJ_Loja',
    tf.CORPORATE_NAME as 'Fornecedor_Razao_Social',
    CASE
        WHEN tdp.FK_DESPESA IS NOT NULL
            THEN 'True'
        ELSE 'False'
    END AS 'Parcelamento',
    CASE 
        WHEN tdp.FK_DESPESA IS NOT NULL
            THEN COUNT(tdp.ID) OVER (PARTITION BY tdr.ID)
        ELSE NULL 
    END AS 'Qtd_Parcelas',
    tdp.PARCELA as 'Num_Parcela',
    tdp.VALOR as 'Valor_Parcela',
    DATE_FORMAT(DATE_ADD(tdp.`DATA`, INTERVAL 30 SECOND), '%d/%m/%Y') as 'Vencimento_Parcela',
    DATE_FORMAT(DATE_ADD(tc.`DATA`, INTERVAL 30 SECOND), '%d/%m/%Y') AS 'Previsao_Parcela',
    DATE_FORMAT(DATE_ADD(tc2.`DATA`, INTERVAL 30 SECOND), '%d/%m/%Y') AS 'Realiz_Parcela',
    tdr.VALOR_PAGAMENTO as 'Valor_Original',
    tdr.VALOR_LIQUIDO as 'Valor_Liquido',
    DATE_ADD(STR_TO_DATE(tdr.LANCAMENTO, '%Y-%m-%d'), INTERVAL 30 SECOND) as 'Data_Lancamento',
    tfdp.DESCRICAO as 'Forma_Pagamento',
    tccg.DESCRICAO as 'Class_Cont_1',
    tccg2.DESCRICAO as 'Class_Cont_2',
    tscd.DESCRICAO as 'Status_Conf_Document',
    tsad.DESCRICAO as 'Status_Aprov_Diret',
    tsac.DESCRICAO as 'Status_Aprov_Caixa',
    CASE
        WHEN tdp.PARCELA_PAGA = 1 
            THEN 'Parcela_Paga'
        ELSE 'Parcela_Pendente'
    END as 'Status_Pgto',
    tcb.NOME_DA_CONTA as 'Conta_Bancaria'
  FROM 
    T_DESPESA_RAPIDA tdr
  INNER JOIN T_EMPRESAS te ON (tdr.FK_LOJA = te.ID)
  LEFT JOIN T_FORMAS_DE_PAGAMENTO tfdp ON (tdr.FK_FORMA_PAGAMENTO = tfdp.ID)
  LEFT JOIN T_FORNECEDOR tf ON (tdr.FK_FORNECEDOR = tf.ID)
  LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 tccg ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = tccg.ID)
  LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 tccg2 ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = tccg2.ID)
  LEFT JOIN T_STATUS_CONFERENCIA_DOCUMENTACAO tscd ON (tdr.FK_CONFERENCIA_DOCUMENTACAO = tscd.ID)
  LEFT JOIN T_STATUS_APROVACAO_DIRETORIA tsad ON (tdr.FK_APROVACAO_DIRETORIA = tsad.ID)
  LEFT JOIN T_STATUS_APROVACAO_CAIXA tsac ON (tdr.FK_APROVACAO_CAIXA = tsac.ID)
  LEFT JOIN T_STATUS_PAGAMENTO tsp ON (tdr.FK_STATUS_PGTO = tsp.ID)
  LEFT JOIN T_DEPESA_PARCELAS tdp ON (tdp.FK_DESPESA = tdr.ID)
  LEFT JOIN T_CONTAS_BANCARIAS tcb ON (tdp.FK_CONTA_BANCARIA = tcb.ID)
  LEFT JOIN T_CALENDARIO tc ON (tdp.FK_PREVISAO_PGTO = tc.ID)
  LEFT JOIN T_CALENDARIO tc2 ON (tdp.FK_DATA_REALIZACAO_PGTO = tc2.ID)
  WHERE 
    tdp.FK_DESPESA IS NOT NULL
    AND (tdr.FK_DESPESA_TEKNISA IS NULL OR tdr.BIT_DESPESA_TEKNISA_PENDENTE = 1)
  ORDER BY 
    tc2.`DATA` DESC
"""

GET_EXTRATOS_BANCARIOS = """
SELECT
teb.ID as 'ID_Extrato_Bancario',
tcb.ID as 'ID_Conta_Bancaria',
tcb.NOME_DA_CONTA as 'Nome_Conta_Bancaria',
te.ID as 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
teb.DATA_TRANSACAO as 'Data_Transacao',
CASE 
    WHEN teb.FK_TIPO_CREDITO_DEBITO = 100 THEN 'CREDITO'
    ELSE 'DEBITO'
END as 'Tipo_Credito_Debito',
teb.DESCRICAO_TRANSACAO as 'Descricao_Transacao',
teb.VALOR as 'Valor'
FROM T_EXTRATOS_BANCARIOS teb
INNER JOIN T_CONTAS_BANCARIAS tcb ON (teb.FK_CONTA_BANCARIA = tcb.ID)
INNER JOIN T_EMPRESAS te ON (tcb.FK_LOJA = te.ID)
WHERE teb.DESCRICAO_TRANSACAO NOT LIKE '%RESG AUTOMATICO%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%APLICACAO AUTOMATICA%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%APLIC.AUTOM.INVESTFACIL*%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%RESG.AUTOM.INVEST FACIL*%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%RESGATE INVEST FACIL%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%APLICACAO CONTAMAX%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%Pix Enviado-Conta Transacional%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%RESGATE CONTAMAX AUTOMATICO%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%APLIC.INVEST FACIL%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%RENTAB.INVEST FACILCRED*%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%BB RENDE FACIL - RENDE FACIL%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%BB RENDE FCIL - RENDE FACIL%'
AND teb.DESCRICAO_TRANSACAO NOT LIKE '%BB RENDE FCIL%'
ORDER BY teb.DATA_TRANSACAO DESC
"""

GET_MUTUOS = """
SELECT
tm.ID as 'Mutuo_ID',
tm.`DATA` as 'Data_Mutuo',
te.ID as 'ID_Casa_Saida',
te.NOME_FANTASIA as 'Casa_Saida',
te2.ID as 'ID_Casa_Entrada',
te2.NOME_FANTASIA as 'Casa_Entrada',
tm.VALOR as 'Valor',
tm.TAG_FATURAM_ZIG as 'Tag_Faturam_Zig'
FROM T_MUTUOS tm 
LEFT JOIN T_EMPRESAS te ON (tm.FK_LOJA_SAIDA = te.ID)
LEFT JOIN T_EMPRESAS te2 ON (tm.FK_LOJA_ENTRADA = te2.ID)
ORDER BY tm.`DATA` DESC
"""

GET_TESOURARIA = """
SELECT
ttt.ID as 'tes_ID',
te.ID as 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
ttt.DATA_TRANSACAO as 'Data_Transacao',
ttt.VALOR as 'Valor',
ttt.DESCRICAO as 'Descricao'
FROM T_TESOURARIA_TRANSACOES ttt 
INNER JOIN T_EMPRESAS te ON (ttt.FK_LOJA = te.ID)
ORDER BY ttt.DATA_TRANSACAO DESC
"""

GET_AJUSTES_CONCILIACAO = """
SELECT 
tac.FK_EMPRESA AS 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
tac.DATA_AJUSTE AS 'Data_Ajuste',
tac.VALOR AS 'Valor',
tac.DESCRICAO AS 'Descrição'
FROM T_AJUSTES_CONCILIACAO tac
INNER JOIN T_EMPRESAS te ON (tac.FK_EMPRESA = te.ID)
"""

