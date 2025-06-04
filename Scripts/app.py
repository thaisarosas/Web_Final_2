import streamlit as st
import pandas as pd
import plotly.express as px
import os

#Maneira que encontrei/entendi de encontrar o caminho do arquivo
#Maneira que encontrei de localizar arquivo no Streamlit
caminho_arquivo = os.path.join(os.path.dirname(__file__), '..', 'Base_Tratada', 'produtos_lolita_pimenta_tratados_2.csv')

#Leitura do CSV
df = pd.read_csv(caminho_arquivo, sep=';')

#Criando um título pra aplicação
st.title('Análise Exploratória de Dados Interativa')

#Criando um texto introdutório
st.markdown('Esta aplicação permite realizar anáises visuais e interativas do banco de dados abaixo, realizando a identificação de padrões, médias e insights importantes.')

#Abrir no Streamlit 
st.dataframe(df)

#====================================================================================================================================
#====================================================================================================================================

# Analisando Nulos
st.subheader('Análise de Nulos')
aux = df.isnull().sum().reset_index()
aux.columns = ['variavel', 'qtd_nulos']
nulos = aux[aux['qtd_nulos'] > 0]

if not nulos.empty:
    st.write('As seguintes colunas possuem valores nulos:')
    st.dataframe(nulos)
else:
    st.write('Não há nulos a ser analisado.')

#====================================================================================================================================
#====================================================================================================================================

#Análises Univariadas
st.header("1. Análises Univariadas")
st.markdown("Explore a distribuição de variáveis numéricas individualmente.")

colunas_numericas_para_analise = df.select_dtypes(include=['number']).columns.tolist()

if 'id_produto' in colunas_numericas_para_analise:
    colunas_numericas_para_analise.remove('id_produto')

# Dropdown para selecionar a coluna
coluna_univariada_selecionada = st.selectbox(
    'Selecione uma coluna para análise univariada:',
    options=colunas_numericas_para_analise,
    index=colunas_numericas_para_analise.index('preco') if 'preco' in colunas_numericas_para_analise else 0
)

if coluna_univariada_selecionada:
    if pd.api.types.is_numeric_dtype(df[coluna_univariada_selecionada]):
        st.subheader(f'Medidas Resumo da Coluna "{coluna_univariada_selecionada}"')
        
        # Calcula as medidas
        if not df[coluna_univariada_selecionada].empty:
            media = df[coluna_univariada_selecionada].mean()
            mediana = df[coluna_univariada_selecionada].median()
            desvio_padrao = df[coluna_univariada_selecionada].std()
            minimo = df[coluna_univariada_selecionada].min()
            maximo = df[coluna_univariada_selecionada].max()

            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)

            # Formatação baseada na coluna
            if coluna_univariada_selecionada == 'preco' or coluna_univariada_selecionada == 'desconto':
                col1.metric("Média", f"R$ {media:.2f}")
                col2.metric("Mediana", f"R$ {mediana:.2f}")
                col3.metric("Desvio Padrão", f"R$ {desvio_padrao:.2f}")
                col4.metric("Mínimo", f"R$ {minimo:.2f}")
                col5.metric("Máximo", f"R$ {maximo:.2f}")
            else:
                col1.metric("Média", f"{media:.2f}")
                col2.metric("Mediana", f"{mediana:.2f}")
                col3.metric("Desvio Padrão", f"{desvio_padrao:.2f}")
                col4.metric("Mínimo", f"{minimo:.2f}")
                col5.metric("Máximo", f"{maximo:.2f}")

            st.markdown(f"**Interpretação:**")
            st.write(f"- A **Média ({media:.2f})** é o valor central. Em '{coluna_univariada_selecionada}', isso representa o valor típico.")
            st.write(f"- A **Mediana ({mediana:.2f})** é o valor do meio quando os dados são ordenados, menos sensível a outliers.")
            st.write(f"- O **Desvio Padrão ({desvio_padrao:.2f})** mede a dispersão dos dados. Um valor alto indica que os dados estão espalhados; um valor baixo, que estão agrupados em torno da média.")
            st.write(f"- O **Mínimo ({minimo:.2f})** e **Máximo ({maximo:.2f})** mostram a amplitude dos valores na coluna.")
        else:
            st.warning(f"O DataFrame filtrado está vazio para a coluna '{coluna_univariada_selecionada}'.")

        st.markdown("---")

        #Histograma
        st.subheader(f'Histograma de {coluna_univariada_selecionada}')
        fig_hist = px.histogram(
            df,
            x=coluna_univariada_selecionada,
            nbins=30,
            title=f'Distribuição de {coluna_univariada_selecionada}'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.write(f"**Interpretação (Histograma):** Este gráfico mostra a frequência com que os valores de '{coluna_univariada_selecionada}' aparecem. Picos indicam valores mais comuns. Uma distribuição simétrica sugere normalidade, enquanto assimetria (caudas) pode indicar outliers ou uma distribuição não-normal.")

        st.markdown("---")

        #Boxplot
        st.subheader(f'Boxplot de {coluna_univariada_selecionada}')
        fig_box = px.box(
            df,
            y=coluna_univariada_selecionada,
            title=f'Boxplot de {coluna_univariada_selecionada}'
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.write(f"**Interpretação (Boxplot):** O boxplot resume a distribuição de '{coluna_univariada_selecionada}'. A caixa central representa o intervalo interquartil (onde 50% dos dados estão). A linha dentro da caixa é a mediana. Os 'bigodes' mostram a dispersão dos dados sem outliers, e os pontos fora dos bigodes são potenciais outliers detectados pelo método do quartil. Ele é útil para visualizar a simetria e a presença de valores extremos.")

    else:
        st.warning(f"A coluna '{coluna_univariada_selecionada}' não é numérica e não pode ser analisada com histograma e boxplot.")
else:
    st.info("Nenhuma coluna numérica disponível para análise univariada.")

#====================================================================================================================================
#====================================================================================================================================

#Análises Multivariadas
st.header("2. Análises Bivariadas e Multivariadas") # Ajustado para "2."
st.markdown("Explore a relação entre duas ou mais variáveis.")

#Obter colunas numéricas e categóricas
colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
colunas_categoricas = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

# Limpar 'id_produto' se existir para evitar que seja plotado como numérica em contextos inadequados
if 'id_produto' in colunas_numericas:
    colunas_numericas.remove('id_produto')

# ====================================================================================================================================

# Scatter Plot
st.subheader('2.1. Scatter Plot: Relação entre Variáveis Numéricas') # Sub-título para clareza
st.write("Selecione duas variáveis numéricas para observar sua correlação. Opcionalmente, adicione uma terceira variável para colorir os pontos.")

if len(colunas_numericas) >= 2:
    # Opções para X e Y
    col_x_scatter = st.selectbox("Eixo X (Scatter Plot):", colunas_numericas, index=colunas_numericas.index('preco') if 'preco' in colunas_numericas else 0, key='scatter_x')
    col_y_scatter = st.selectbox("Eixo Y (Scatter Plot):", colunas_numericas, index=colunas_numericas.index('desconto') if 'desconto' in colunas_numericas else (1 if len(colunas_numericas) > 1 else 0), key='scatter_y')

    # Opção para cor (multivariada)
    opcoes_cor = ['Nenhum'] + colunas_categoricas + colunas_numericas
    col_color_scatter = st.selectbox("Colorir por (Opcional):", opcoes_cor, key='scatter_color')

    if col_x_scatter and col_y_scatter:
        color_col = col_color_scatter if col_color_scatter != 'Nenhum' else None
        
        fig_scatter = px.scatter(
            df,
            x=col_x_scatter,
            y=col_y_scatter,
            color=color_col,
            title=f'Gráfico de Dispersão: {col_x_scatter} vs {col_y_scatter}' + (f' por {color_col}' if color_col else ''),
            hover_data=df.columns
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.write(f"**Interpretação (Scatter Plot):** Este gráfico de dispersão mostra a relação entre '{col_x_scatter}' e '{col_y_scatter}'. Cada ponto representa um produto. Podemos observar se há uma correlação (positiva, negativa ou nenhuma). Se uma variável foi usada para colorir, ela ajuda a identificar padrões em três dimensões.")
    else:
        st.warning("Por favor, selecione duas colunas numéricas para o Scatter Plot.")
else:
    st.info("Não há colunas numéricas suficientes (mínimo 2) para gerar o Scatter Plot.")

st.markdown("---")

# ====================================================================================================================================

# Análise Multivariada Adicional
st.header("3. Análise Multivariada (Matriz de Correlação)")
st.write("A matriz de correlação mostra a força e a direção da relação linear entre pares de variáveis numéricas.")

if len(colunas_numericas) >= 2:
    corr_matrix = df[colunas_numericas].corr(numeric_only=True)
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=px.colors.sequential.RdBu, # Escolha de escala de cores
        title='Matriz de Correlação entre Variáveis Numéricas'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    st.write(f"**Interpretação (Matriz de Correlação):** Os valores variam de -1 a 1. Valores próximos de 1 indicam uma forte correlação positiva (quando um aumenta, o outro também). Valores próximos de -1 indicam forte correlação negativa (quando um aumenta, o outro diminui). Valores próximos de 0 indicam pouca ou nenhuma correlação linear. Esta matriz ajuda a identificar quais variáveis se movem juntas.")
else:
    st.info("Não há colunas numéricas suficientes para gerar a Matriz de Correlação.")  