import pandas as pd
import streamlit as st
import plotly.express as px

# função para carregar o dataset
@st.cache_data
def get_data():
    return pd.read_csv("venture_capital.csv")

# função para treinar o modelo
def train_model():
    data = get_data()
    data = data.drop(columns="Startup")
    
    #Separando os Dados de Treino e de Teste
    X = data.iloc[:,:-1].values
    y = data.iloc[:,-1].values

    #Redimensionando os Dados - Padronização com o StandardScaler
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_trans = sc.fit_transform(X)

    #Treinamento da Máquina Preditiva
    from sklearn.svm import SVC
    Maquina_preditiva = SVC(kernel='linear', gamma=1e-5, C=10, random_state=7)
    Maquina_preditiva.fit(X_trans, y)
    return Maquina_preditiva

# criando um dataframe
data = get_data()

# treinando o modelo
model = train_model()

# título
st.title("Indicação de Investimento em Startup - Desenvolvido por Evandro Costa")

# subtítulo
st.markdown("Este é um Aplicativo utilizado para exibir a solução de Ciência de Dados para o problema de Investimentos em Startups em Venture Capital.")

st.sidebar.subheader("Insira os Dados dos Indicadores da Startup Avaliada")

# mapeando dados do usuário para cada atributo
Indice_Faturamento = st.sidebar.number_input("Índice de Faturamento", value=data.Indice_Faturamento.mean())
Indice_Setorial = st.sidebar.number_input("Projecao Setorial", value=data.Indice_Setorial.mean())
Indice_Inovacao = st.sidebar.number_input("Índice de Inovação", value=data.Indice_Inovacao.mean())
Indice_Falencias = st.sidebar.number_input("Índice de Falências", value=data.Indice_Falencias.mean())
Indice_Expertise_Estrategica = st.sidebar.number_input("Indicador de Expertise Estratégica", value=data.Indice_Expertise_Estrategica.mean())

# inserindo um botão na tela
btn_predict = st.sidebar.button("Avaliação da Startup Investida")

# verificando o dataset
st.subheader("Selecionando as Variáveis de Avaliação da Startup")

# atributos para serem exibidos por padrão
defaultcols = ['Indice_Faturamento','Indice_Setorial','Indice_Inovacao','Indice_Falencias','Indice_Expertise_Estrategica']

# defindo atributos a partir do multiselect
cols = st.multiselect("Atributos", data.columns.tolist(), default=defaultcols)

# exibindo os top 8 registro do dataframe
st.dataframe(data[cols].head(7))

# verifica se o botão foi acionado
if btn_predict:
    result = model.predict([[Indice_Faturamento,Indice_Setorial,Indice_Inovacao,Indice_Falencias,Indice_Expertise_Estrategica]])
    st.subheader("O Investimento na Startup é de :")
    result = result[0]
    st.write(result)