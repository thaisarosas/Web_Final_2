from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv

navegador = webdriver.Chrome()

navegador.get('https://www.lolitapimenta.com.br/calcados/sandalia')

lista_produtos = []
for pagina in range(1,6):
        url_pagina = f"https://www.lolitapimenta.com.br/calcados/sandalia?page={pagina}"
        navegador.get(url_pagina)
        time.sleep(10)
        for produto in range(1,31):
            try:
                dado_produto = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{produto}]/section/a/article/div/div[3]/div/h3/span').text
                print(dado_produto)
                lista_produtos.append(dado_produto)
            except:
                pass

lista_desconto = []
for pagina in range(1,6):
    url_pagina = f"https://www.lolitapimenta.com.br/calcados/sandalia?page={pagina}"
    navegador.get(url_pagina)
    time.sleep(10)
    for desconto in range(1,31):
        try:
            dado_desconto = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{desconto}]/section/a/article/div/div[4]/div[2]/span/span/span').text
            print(dado_desconto)
            lista_desconto.append(dado_desconto)
        except:
                pass
        
lista_preco = []
for pagina in range(1,6):
    url_pagina = f"https://www.lolitapimenta.com.br/calcados/sandalia?page={pagina}"
    navegador.get(url_pagina)
    time.sleep(10)
    for preco in range(1,31):
        try:
            dado_preco = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{preco}]/section/a/article/div/div[4]/div[1]/span/span/span').text
            print(dado_preco)
            lista_preco.append(dado_preco)
        except:
                pass
        
lista_produtos

lista_preco

lista_desconto

tabela_produtos = pd.DataFrame(lista_produtos, columns=['produto'])
tabela_produtos

tabela_desconto = pd.DataFrame(lista_desconto, columns=['desconto'])
tabela_desconto

tabela_preco = pd.DataFrame(lista_preco, columns=['preco'])
tabela_preco

df = pd.concat([tabela_produtos, tabela_desconto, tabela_preco], axis=1)
df

navegador.quit()

#Tratando os dados da coluna preço, removendo R$, e vírgula por ponto
df['preco'] = (
    df['preco']
    .str.replace('R$', '', regex=False)     
    .str.replace('.', '', regex=False)      
    .str.replace(',', '.', regex=False)     
    .astype(float)                          
)

#Tratando os dados da coluna preço, removendo R$, e vírgula por ponto
df['desconto'] = (
    df['desconto']
    .str.replace('R$', '', regex=False)     # remove o 'R$'
    .str.replace('.', '', regex=False)      # remove separadores de milhar
    .str.replace(',', '.', regex=False)     # troca vírgula por ponto decimal
    .astype(float)                          # converte para float
)

# nulos
df.preco.fillna(0, inplace=True)
df.desconto.fillna(0, inplace=True)
df.produto.fillna('missing', inplace=True)

# duplicatas
df = df.drop_duplicates()

#outliers preco
df.loc[df['preco'] > 999, 'preco'] = 999
df.loc[df['preco'] < 0, 'preco'] = 100

#outliers desconto
df.loc[df['desconto'] > 999, 'desconto'] = 999
df.loc[df['desconto'] < 0, 'desconto'] = 10

df

#df.to_csv('produtos_lolita_pimenta.csv', sep=';', index=False, encoding='utf-8')
df.to_csv('../Base_Tratada/produtos_lolita_pimenta_tratados_2.csv', sep=';', index=False, encoding='utf-8')