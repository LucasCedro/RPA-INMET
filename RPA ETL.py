import pandas as pd
import os


proj = "cerne" #Alterar aqui

if proj == "plateau":
    # definindo o diretório de download
    ref_dir = "C:\\Users\\LUCASCEDROTEMPONI\\Innovatech Gestão Empresarial e Agroflorestal Ltda\\PLATEAU GREEN - Documents\\15. PLATAFORMA IRIS\\02. BANCO DE DADOS\\02. SILVICULTURA\\"
    
elif proj == "cerne":
    # definindo o diretório de download
    ref_dir = "C:\\Users\\LUCASCEDROTEMPONI\\Amata S A\\AMATA PR - Documentos AMATA\\09. MONITORAMENTO E CONTROLE\\03. DASHBOARD BI\\02. BANCO DE DADOS\\00. CONSULTAS AUXILIARES\\"

else:
    print("Projeto nao encontrado")
    sys.exit()


# criar os DataFrames para as tabelas
df1 = pd.read_excel(ref_dir + 'Base_Temperatura.xlsx')
df2 = pd.read_csv(ref_dir + 'dados_inmet.csv', na_values='', delimiter=';' ,decimal=',')

# renomear as colunas da segunda tabela
df2 = df2.rename(columns={
    'Pressao Ins. (hPa)': 'PRE_INST',
    'Pressao Max. (hPa)': 'PRE_MAX',
    'Radiacao (KJ/m²)': 'RAD_GLO',
    'Pto Orvalho Ins. (C)': 'PTO_INT',
    'Temp. Min. (C)': 'TEM_MIN',
    'Pto Orvalho Max. (C)': 'PTO_MAX',
    'Dir. Vento (m/s)': 'VEM_DIR',
    'Chuva (mm)': 'CHUVA',
    'Pressao Min. (hPa)': 'PRE_MIN',
    'Umi. Max. (%)': 'UMD_MAX',
    'Vel. Vento (m/s)': 'VEN_VEL',
    'Pto Orvalho Min. (C)': 'PTO_MIN',
    'Temp. Max. (C)': 'TEM_MAX',
    'Raj. Vento (m/s)': 'VEM_RAJ',
    'Temp. Ins. (C)': 'TEM_INS',
    'Umi. Ins. (%)': 'UMD_INS',
    'Hora (UTC)': 'HR_MEDICAO',
    'Umi. Min. (%)':'UMD_MIN',
    'Data':'DT_MEDICAO'
})

# converter a coluna de data para o formato yyyy-mm-dd
df2['DT_MEDICAO'] = pd.to_datetime(df2['DT_MEDICAO'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

if proj == "plateau":
    # definindo o diretório de download
    df2 = df2.assign(DC_NOME='Ribas do Rio Pardo', LV_LATITUDE=-20.46666666, UF='MS', VL_LONGITUDE=-53.76305555, CD_ESTACAO='A756')

elif proj == "cerne":
    # definindo o diretório de download
    df2 = df2.assign(DC_NOME='COLOMBO', LV_LATITUDE=-25.322464, UF='PR', VL_LONGITUDE=-49.157733, CD_ESTACAO='B806')
    
else:
    print("Projeto nao encontrado")
    sys.exit()


# concatenar as duas tabelas
df_concat = pd.concat([df1, df2], axis=0, ignore_index=True)

# salvar a tabela concatenada no arquivo original
df_concat.to_excel(ref_dir + 'Base_Temperatura.xlsx', index=False)

os.remove(ref_dir + 'dados_inmet.csv')