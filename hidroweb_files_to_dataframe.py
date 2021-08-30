import pandas as pd
from datetime import datetime
#from tkinter import messagebox
import numpy as np

BASE_URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'

def Dataframe_from_txt_Hidroweb_VAZAO(filename):
    """
    Entrada:
        - filename: Nome do arquivo de Vazao do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Nivel de Consistência e Vazao
                Sendo o index do dataframe a Data da medição.
    """
    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[9], engine='python', decimal=",")
    # As colunas 'NivelConsistencia' e 'EstacaoCodigo' correspondem a data e hora
    dt = dt.set_index(['NivelConsistencia', 'EstacaoCodigo'])
    # Pega a matriz de dados e coloca a coluna com o número do dia da medição
    dt = dt.iloc[:, 13:44]
    dt.columns = range(1, 32)

    return checagem_final_hidroweb(dt, 'Vazao')


def Dataframe_from_txt_Hidroweb_CHUVA(filename):
    """
    Entrada:
        - filename: Nome do arquivo de Vazao do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Nivel de Consistência e Vazao
                Sendo o index do dataframe a Data da medição.
    """
    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[8], engine='python', decimal=",")
    # As colunas 'NivelConsistencia' e 'EstacaoCodigo' correspondem a data e hora
    dt = dt.set_index(['NivelConsistencia', 'EstacaoCodigo'])
    # Pega a matriz de dados e coloca a coluna com o número do dia da medição
    dt = dt.iloc[:, 10:41]
    dt.columns = range(1, 32)

    return checagem_final_hidroweb(dt, 'Chuva')


def Dataframe_from_txt_Hidroweb_NIVEL(filename):
    """
    Entrada:
        - filename: Nome do arquivo de Vazao do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Nivel de Consistência e Vazao
                Sendo o index do dataframe a Data da medição.
    """
    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[9], engine='python', decimal=",")
    # As colunas 'NivelConsistencia' e 'EstacaoCodigo' correspondem a data e hora
    dt = dt.set_index(['NivelConsistencia', 'EstacaoCodigo'])
    # Pega a matriz de dados e coloca a coluna com o número do dia da medição
    dt = dt.iloc[:, 13:44]
    dt.columns = range(1, 32)

    return checagem_final_hidroweb(dt, 'Nivel')


def Dataframe_from_txt_Hidroweb_SEDIMETOS(filename):
    """
    Entrada:
        - filename: Nome do arquivo de sedimentos do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Hora, Vazao, Area Molhada, Largura, Velocidade e Concentração
                Sendo o index do dataframe a data da amostragem.
    """

    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[6], engine='python', decimal=",")
    # Reseta o index
    dt = dt.reset_index(drop=True)
    # Cria o dataframe só com dados de:
    # Data, Hora, Vazão, Área Molhada, Largura, Velocidade, Concentração
    dt = dt.iloc[:, [0, 1, 2, 8, 9, 10, 11, 12]]
    dt.columns = ['Nivel_Consistencia','Data', 'Hora', 'Vazao', 'Area Molhada', 'Largura', 'Velocidade', 'Concentracao']

    dt['Hora'] = dt['Hora'].map(lambda x: str(x)[11:])

    # Exclui ou substitue os NaNs ou vazios
    dt = dt.dropna(subset=['Data'])
    dt.replace('', '00:00:00', inplace=True)
    dt['Hora'] = dt['Hora'].fillna('00:00:00')
    # Soma a data e tempo como strings
    dt['Data'] = dt['Data'].astype(str) + ' ' + dt['Hora'].astype(str)
    del dt['Hora']

    return checagem_final_hidroweb_2(dt)


def Dataframe_from_txt_Hidroweb_QUALIDADE(filename):
    """
    Entrada:
        - filename: Nome do arquivo de sedimentos do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Hora, Vazao, Area Molhada, Largura, Velocidade e Concentração
                Sendo o index do dataframe a data da amostragem.
    """

    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, index_col=None, sep=";", header=[10], engine='python', decimal=",")
    # Reseta o index
    dt = dt.reset_index(drop=True)
    # Cria o dataframe só com dados de:
    # Data, Hora, Vazão, Área Molhada, Largura, Velocidade, Concentração

    # O nome das colunas com os dado reais estao desalinhados e precisa arrumar, por isso essas duas linhas
    dt = dt.iloc[:, [0, 1, 2, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 39, 41, 42, 43, 59, 124, 132]]
    dt.columns = ['Nivel_Consistencia',
                  'Data',
                  'Hora',
                  'Prof',
                  'T_Ar',
                  'T_Amostra',
                  'pH',
                  'Cor',
                  'Turb',
                  'Cond',
                  'Dureza_T',
                  'Dureza',
                  'DQO',
                  'DBO',
                  'OD',
                  'ST',
                  'SF',
                  'SV',
                  'SST',
                  'SSF',
                  'SSV',
                  'SDT',
                  'SDF',
                  'SDV',
                  'SSed',
                  'Alc_CO3',
                  'Alc_HCO3',
                  'Alc_OH',
                  'Cloretos',
                  'SO2',
                  'S2',
                  'Fluoretos',
                  'PO4_T',
                  'NT',
                  'NH3',
                  'NO3',
                  'NO2',
                  'Col',
                  'N_Org',
                  'PT'
                  ]

    dt['Hora'] = dt['Hora'].map(lambda x: str(x)[11:])

    # Exclui ou substitue os NaNs ou vazios
    dt = dt.dropna(subset=['Data'])
    dt.replace('', '00:00:00', inplace=True)
    dt['Hora'] = dt['Hora'].fillna('00:00:00')

    # Soma a data e tempo como strings
    dt['Data'] = dt['Data'].astype(str) + ' ' + dt['Hora'].astype(str)
    del dt['Hora']

    return checagem_final_hidroweb_2(dt)

def Dataframe_from_txt_Hidroweb_RESUMO_DESCARGA(filename):

    dt = pd.read_csv(filename, sep="\t|;", header=[6], engine='python', decimal=",")

    dt.columns = ['NivelConsistencia', 'Data', 'Hora', 'NumMedicao', 'Cota', 'Vazao', 'AreaMolhada', 'Largura',
                   'VelMedia', 'Profundidade', 'datains', 'dataalt', 'respalt', 'tecnico', 'medidorvazao',
                   'algumacoisa']

    dt = dt[['NivelConsistencia', 'Data', 'Hora', 'Cota', 'Vazao', 'AreaMolhada', 'Largura', 'VelMedia', 'Profundidade']]

    dt['Data'] = pd.to_datetime(dt['Data'] + ' ' + dt['Hora'].str.replace('01/01/1900 ', ''), format='%d/%m/%Y %H:%M:%S')

    del dt['Hora']

    dt = dt.set_index('Data').T

    return dt


def Dataframe_from_txt_Hidroweb_PERFIL_TRANSVERSAL(filename):

    list_dts = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i > 11:
                line = line.replace('|', '')
                line = line.replace(',', '.')
                tudo = line.split(";")[1:]

                if tudo[2] != '':
                    horas = datetime.strptime(tudo[2], '%d/%m/%Y %H:%M:%S')
                    date = datetime.strptime(tudo[1], '%d/%m/%Y') + timedelta(hours=horas.hour, minutes=horas.minute,
                                                                              seconds=horas.second)
                else:
                    date = datetime.strptime(tudo[1], '%d/%m/%Y').date()

                # Exclue a data e hora, pq já foi guardada em outra variável
                tudo.pop(1)
                tudo.pop(1)

                tudo[-1] = tudo[-1].strip()

                complemento = tudo[:11]

                n_verticais = int(complemento[3])
                verticais = tudo[-n_verticais * 2 - 1:-1]

                distancias = np.array(verticais[0:][::2], dtype=np.float32)
                profundidades = np.array(verticais[1:][::2], dtype=np.float32)
                # Só separa se tiver dados

                nomes = ['Data', 'NivelConsistencia', 'NumLevantamento', 'TipoSecao', 'NumVerticais', 'DistanciaPIPF', 'EixoXDistMaxima', 'EixoXDistMinima', 'EixoYCotaMaxima', 'EixoYCotaMinima', 'ElmGeomPassoCota', 'Observacoes', '']
                dados = [[date]] + [[i] for i in complemento] + [['Distancia', 'Profundidade']]

                index = pd.MultiIndex.from_product(dados, names=nomes)
                dt_comp = pd.DataFrame([distancias, profundidades], index=index)
                dt_comp.columns = 'Medição ' + dt_comp.columns.astype(str)
                list_dts.append(dt_comp)

    dt = pd.concat(list_dts, axis=0).T.sort_index(axis=1)

    return dt.round(2)

def format_Date(data):
    try:
        return datetime.strptime(data, '%d/%m/%Y')
    except ValueError:
        try:
            return datetime.strptime(data, '%d/%m/%Y %H:%M')
        except ValueError:
            try:
                return datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                print(data)
                print('AVISO: formato de data não existe: data foi excluida')
                #messagebox.showinfo('AVISO: formato de data não existe: data foi excluida')
                return np.nan


def checagem_final_hidroweb(dt, name):
    dt = dt.stack().to_frame()

    dt = dt.dropna()

    Data = [str(ix[2]) + ix[0][2:] for ix in dt.index.tolist()]
    NC = [int(ix[1]) for ix in dt.index.tolist()]

    dt.index = pd.Index(Data)

    dt.index = dt.index.to_series().apply(lambda x: format_Date(x))

    dt.index.name = 'Data'
    dt.columns = [name]

    dt['Nivel_Consistencia'] = NC
    dt = dt.loc[dt.index.notna()]

    dt = dt.iloc[:, ::-1]

    # Checa se existe algum nível de consistência diferente de 1 e 2
    for nivel in list(dt['Nivel_Consistencia']):
        if (nivel != 1) and (nivel != 2):
            print("AVISO", "Existem Níveis de consistência diferentes de 1 e 2")
            #messagebox.showinfo("AVISO", "Existem Níveis de consistência diferentes de 1 e 2")
            break

    # Organizará as datas e os níveis de consistência em ordem crescente
    # Excluirá os dados com data repetida, mantendo sempre o último valor da lista
    dt = dt.sort_values(by=['Data', 'Nivel_Consistencia'], ascending=[True, True])
    dt = dt[~dt.index.duplicated(keep='last')]

    return dt

def checagem_final_hidroweb_2(dt):
    # Acerta o formato da data
    dt['Data'] = dt['Data'].apply(lambda x: format_Date(x))
    dt = dt.loc[dt.index.notna()]

    # Coloca a Data como index do dataframe
    dt = dt.set_index('Data')
    dt = dt.sort_index()

    # Checa se existe algum nível de ocnsistência diferente de 1 e 2
    for nivel in list(dt['Nivel_Consistencia']):
        if (nivel != 1) and (nivel != 2):
            print("AVISO", "Existem Níveis de consistência diferentes de 1 e 2")
            #messagebox.showinfo("AVISO", "Existem Níveis de consistência diferentes de 1 e 2")
            break

    # Organizará as datas e os níveis de consistência em ordem crescente
    # Excluirá os dados com data repetida, mantendo sempre o último valor da lista
    dt = dt.sort_values(by=['Data', 'Nivel_Consistencia'], ascending=[True, True])
    dt = dt[~dt.index.duplicated(keep='last')]
    return dt
    
# f = '.../Estacoes/vazoes_T_64634000.txt'
# dt_vazao = io.Dataframe_from_txt_Hidroweb_VAZAO(f)

# f = '.../Estacoes/cotas_T_64634000.txt'
# dt_nivel = io.Dataframe_from_txt_Hidroweb_NIVEL(f)

# f = '.../Estacoes/sedimentos_T_64634000.txt'
# dt_sed = io.Dataframe_from_txt_Hidroweb_SEDIMETOS(f)

# f = '.../Estacoes/2248032/chuva.txt'
# dt_chuva = io.Dataframe_from_txt_Hidroweb_CHUVA(f)

# f = '.../Estacoes/qualagua_T_64545700.txt'
# dt_quali = io.Dataframe_from_txt_Hidroweb_QUALIDADE(f)    
