import streamlit as st
import pandas as pd
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go

countries = ['brazil','united states'] # lista de países
intervals = ['Daily', 'Weekly', 'Monthly'] #Lista de intervalos

start_date = datetime.today() - timedelta(days=30) #Data inicial recebe data de hoje menos 30 dias
end_date = datetime.today() # Data de fim recebe a data de hoje

@st.cache(allow_output_mutation=True)# O Streamlit fornece um mecanismo de cache que permite que seu aplicativo mantenha o desempenho mesmo ao carregar dados da Web
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)# Funcão recebe os parametros stock, pais, data inicial, data final e intervalo
    return df # Retorna um dataframe

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig


# CRIANDO UM WIDGET DE BARRA LATERAL
barra_lateral = st.sidebar.empty()

# CRIANDO UM WIDGET DE SELEÇÃO NA BARRA LATERAL
country_select = st.sidebar.selectbox("Selecione o país:", countries)

# PEGAR AS AÇÕES DOS PAISES 
acoes = ip.get_stocks_list(country=country_select)# A VARIAVEL COUNTRY(PAIS) RECEBE ELEMENTO DA BARRA LATERAL DO PAIS SELECIONADO

# SELECIONAR O ATIVO
stock_select = st.sidebar.selectbox("Selecione o ativo:", acoes)# PEGA O RETORNO DE LISTAS DA VARIAVEL ACOES

from_date = st.sidebar.date_input('De:', start_date)# Data inicial
# O COMANDO DATE_INPUT Exibe um widget de entrada de data.

to_date = st.sidebar.date_input('Para:', end_date)#Data final

interval_select = st.sidebar.selectbox("Selecione o interval:", intervals)# CRIANDO UM WIDGET DE SELEÇÃO NA BARRA LATERA

#Exiba um widget de caixa de seleção.
carregar_dados = st.sidebar.checkbox('Carregar dados')



# elementos centrais da página
st.title('Monitorar Ações')#Exibe o texto na formatação do título. IGUAL H1 DO HTML

st.subheader('Visualização gráfica')#Exibe o texto na formatação de subcabeçalho. IGUAL H3 DO HTML

# st.empty Insire um contêiner de elemento único.
grafico_line = st.empty() #GRAFICO DE LINHA

# st.empty Insire um contêiner de elemento único.
grafico_candle = st.empty() #GRAFICO DE CANDLE

if from_date > to_date: #SE DATA INICIO MAIOR QUE DATA FINAL EXIBIR UMA MENSAGEM DE ERRO
    st.sidebar.error('Data de ínicio maior do que data final')
else: # SE NÃO EXECUTA A FUNÇÃO CONSULTAR AÇÃO
    df = consultar_acao(stock_select, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    try: # Se nenhuma exceção ocorrer, a cláusula except será ignorada e a execução da try instrução será concluída.
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)# Exiba um gráfico de candle. Recebe a função de fig
        grafico_line = st.line_chart(df.Close)#Exibir um gráfico de linhas.Que carrega um vetor de dados do dataframe(No caso a coluna Close do dataframe)
        if carregar_dados: #Se o elemento checkbox estiver marcado
            st.subheader('Dados') # Carregar o h2 com a mensagem dados
            dados = st.dataframe(df) # Passando o dataframe
            stock_select = st.sidebar.selectbox
     
    except Exception as e: #Se ocorrer uma exceção durante a execução da trycláusula, o restante da cláusula será ignorado.E a cláusula except será executada
        st.error(e)           
           
            
#BAIXANDO DADOS EM CSV
my_large_df = df
@st.cache
def convert_df_to_csv(df):
  # IMPORTANTE: armazenar a conversão em cache para evitar a computação em cada reexecução
    return df.to_csv().encode('utf-8')

csv = convert_df_to_csv(my_large_df)

st.sidebar.download_button(
    label="Baixar dados CSV",
    data=csv,
    file_name='dados_df.csv',
    mime='text/csv',
    help='clique aqui para baixar os dados da planilha csv',
)            
    
        

