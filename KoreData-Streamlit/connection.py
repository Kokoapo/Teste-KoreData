import streamlit as st
import pandas as pd

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM retail;', ttl="10m")

# New Columns
df['Year'] = pd.Series(df['InvoiceDate']).apply(lambda x: x.year)
df['Month'] = pd.Series(df['InvoiceDate']).apply(lambda x: x.month)
df['Day'] = pd.Series(df['InvoiceDate']).apply(lambda x: x.day)
df['TotalPrice'] = df['UnitPrice'] * df['Quantity']

# Queries
query_clientes_ativos = df[~df['InvoiceNo'].str.startswith('C') & df['CustomerID'].notna()]
query_trans_ativas = df[~df['InvoiceNo'].str.startswith('C')]
query_trans_devolvidas = df[df['InvoiceNo'].str.startswith('C')]

# Group By
gb_receita_pais = df.groupby(by='Country')['TotalPrice'].sum()
gb_receita_dia = df.groupby(by='Day')['TotalPrice'].sum()
gb_receita_mes = df.groupby(by='Month')['TotalPrice'].sum()
gb_top_clientes = query_clientes_ativos.groupby(by='CustomerID')['TotalPrice'].sum().nlargest(10)
gb_top_produtos_vendidos = query_trans_ativas.groupby(by='StockCode')['Quantity'].sum().nlargest(10)
gb_top_produtos_devolvidos = query_trans_devolvidas.groupby(by='StockCode')['Quantity'].sum().nsmallest(10)

# Display Information
st.write("# Indicadores de Vendas")
st.write("## Receita por País")
st.bar_chart(gb_receita_pais)
st.write("## Receita por Dia")
st.bar_chart(gb_receita_dia)
st.write("## Receita por Mês")
st.bar_chart(gb_receita_mes)
st.write("## Receita Total")
st.write('${valor:.2f} de receita'.format(valor = df['TotalPrice'].sum()))

st.write("# Indicadores de Clientes")
st.write("## Top Clientes")
st.bar_chart(gb_top_clientes)
st.write("## Clientes Únicos")
st.write('{valor} clientes únicos'.format(valor = query_clientes_ativos['CustomerID'].nunique()))

st.write("# Indicadores de Produtos")
st.write("## Top Produtos Mais Vendidos")
st.bar_chart(gb_top_produtos_vendidos)
st.write("## Top Produtos Mais Devolvidos")
st.bar_chart(gb_top_produtos_devolvidos)

st.write("# Indicadores de Transações")
st.write("## Total de Transações")
st.write('{valor} transações'.format(valor = df['InvoiceNo'].nunique()))
st.write('## Total de Transações com Devolução')
st.write('{valor} transações'.format(valor = query_trans_devolvidas['InvoiceNo'].nunique()))
st.write('## Ticket Médio')
st.write('{valor:.2f}'.format(valor = query_trans_ativas['TotalPrice'].sum() / query_trans_ativas['InvoiceNo'].nunique()))