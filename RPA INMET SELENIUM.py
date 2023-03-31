import os
import sys
import time
from datetime import date, timedelta, datetime

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

import pandas as pd
#----------- esses aqui em baixo podem ser usados com melhor performance ----------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Esse bloco é temporário. Apenas para selecionar qual projeto vamos buscar
proj = "cerne" #Alterar aqui


if proj == "plateau":
    # definindo o diretório de download
    download_dir = "C:\\Users\\LUCASCEDROTEMPONI\\Innovatech Gestão Empresarial e Agroflorestal Ltda\\PLATEAU GREEN - Documents\\15. PLATAFORMA IRIS\\02. BANCO DE DADOS\\02. SILVICULTURA\\"
    estacao = 'AGUA CLARA (A756)'
    cod_estacao = 'A756'
    
elif proj == "cerne":
    # definindo o diretório de download
    download_dir = "C:\\Users\\LUCASCEDROTEMPONI\\Amata S A\\AMATA PR - Documentos AMATA\\09. MONITORAMENTO E CONTROLE\\03. DASHBOARD BI\\02. BANCO DE DADOS\\00. CONSULTAS AUXILIARES\\"
    estacao = 'COLOMBO (B806)'
    cod_estacao = 'B806'
    
else:
    print("Projeto nao encontrado")
    sys.exit()


# In[3]:


# definindo o nome do arquivo a ser baixado
file_name = 'generatedBy_react-csv.csv'

# Define o dia de ontem como ultimo dia a ter informações coletadas
yesterday = date.today() - timedelta(days=1)

# formatar a data como string no formato "dd/mm/yyyy"
yesterday_str = yesterday.strftime('%d/%m/%Y')


#Carrega a base de dados atual
df1 = pd.read_excel(download_dir + 'Base_Temperatura.xlsx')


# obter a data da última medição, ou seja, a primeira data a ser buscada no RPA
primeira_data = df1.iloc[df1.shape[0] - 1]["DT_MEDICAO"]
primeira_data = datetime.strptime(primeira_data, '%Y-%m-%d')
primeira_data = primeira_data.strftime('%d/%m/%Y')


if primeira_data == yesterday_str:
    print("A última data é igual a yesterday")
    sys.exit()


# verifica se o arquivo já existe e remove se existir
if os.path.exists(download_dir + 'dados_inmet.csv'):
    os.remove(download_dir + 'dados_inmet.csv')


# inicia o driver do Chrome com drive atualizado
servico = Service(ChromeDriverManager().install())

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument('--headless')
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

browser = webdriver.Chrome(service=servico, options=chrome_options)

# acessa a página
browser.get(f'https://tempo.inmet.gov.br/TabelaEstacoes/{cod_estacao}')


# espera a página ser carregada
time.sleep(3)


#Abre o menu clicando no botão
browser.find_element('xpath', '//*[@id="root"]/div[1]/div[1]/i').click()
time.sleep(1)


# preenche o campo de estação
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[3]/i').click()
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[3]/input').send_keys(estacao)

# Preenche a Data de Inicio
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').click()
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').clear()
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').send_keys(primeira_data)
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').send_keys(Keys.ENTER)

# Preenche a Data Fim
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').click()
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').clear()
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').send_keys(yesterday_str)
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').send_keys(Keys.ENTER)

# espera a página ser carregada
time.sleep(3)

# Clica no botão "Gerar Tabela"
browser.find_element('xpath', '//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

# tempo máximo que o loop irá esperar pelo elemento em segundos
tempo_maximo = 60

while tempo_maximo > 0:
    try:
        # Tenta encontrar o elemento com o xpath especificado
        elemento = WebDriverWait(browser, 1).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div/div/span/a'))
        )
        # Se encontrou o elemento, clica no botão e sai do loop
        elemento.click()
        break
    except:
        # Se o elemento ainda não está visível na página, espera mais 1 segundo
        tempo_maximo -= 1
        time.sleep(1)

# esperando o arquivo ser baixado
while not os.path.exists(download_dir + file_name):
    time.sleep(1)


# renomeando o arquivo
new_file_name = 'dados_inmet.csv'
os.rename(download_dir + file_name, download_dir + new_file_name)


download_dir + file_name


# fecha o driver
browser.quit()