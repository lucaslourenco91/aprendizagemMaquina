
#----------------------------importando pacotes de bibliotecas do Python------------------------------------
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import re

#----------------------------Configuração do relatório de Log---------------------------------------------
logging.basicConfig(filename='log_acoes.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# --------------------------Solicita nome do usuário------------------------------------------------------
nome_usuario = input("Digite seu nome: ")
while not re.match(r'^[A-Za-z]{3,}( [A-Za-z]{3,})*$', nome_usuario):
    print("Nome inválido. Deve conter apenas letras e pelo menos 3 caracteres por parte.")
    nome_usuario = input("Digite seu nome: ")

logging.info(f"Usuário '{nome_usuario}' iniciou o sistema.")

# --------------------------Solicita o caminho do arquivo------------------------------------------------

df = None 

while True:
    caminho = input("Digite o caminho do arquivo CSV a ser analisado (ou 000 para  do programa): ")

    if caminho == "000":
        print("Encerrando o programa...")
        break

    if not os.path.exists(caminho):
        print("Arquivo não encontrado ou caminho inválido.")
        logging.error(f"{nome_usuario} forneceu caminho do arquivo inválido inválido: {caminho}")
    else:
        try:
            if caminho.endswith('.csv'):
                df = pd.read_csv(caminho)
            elif caminho.endswith('.json'):
                df = pd.read_json(caminho)
            else:
                print("Formato de arquivo não suportado. Use CSV ou JSON.")
                logging.warning(f"{nome_usuario} tentou carregar formato não suportado: {caminho}")
                continue

            print("Arquivo carregado com sucesso!")
            break  

        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            logging.error(f"{nome_usuario} teve erro ao carregar arquivo: {e}")


#------------------------------Limpeza de dados---------------------------------------------------------
if df is not None:
    print("\n--- Iniciando limpeza dos dados ---")

    col_educacao_pais = [col for col in df.columns if 'parent' in col.lower() and 'education' in col.lower()]
    if col_educacao_pais:
        col_edu = col_educacao_pais[0]
        antes = len(df)
        df = df.dropna(subset=[col_edu]).copy()
        depois = len(df)
        print(f"Registros removidos por educação dos pais vazia: {antes - depois}")
    else:
        print("Coluna de educação dos pais não encontrada. Nenhum registro removido.")

    col_attendance = [col for col in df.columns if 'attendance' in col.lower()]
    if col_attendance:
        col_att = col_attendance[0]
        mediana = df[col_att].median()
        df.loc[:, col_att] = df[col_att].fillna(mediana)
        print(f"Valores nulos em '{col_att}' preenchidos com a mediana: {mediana}")
        print(f"Soma total de Attendance: {df[col_att].sum()}")
    else:
        print("Coluna 'Attendance' não encontrada.")

    logging.info(f"{nome_usuario} limpou os dados do DataFrame.")

#---------------------------- Consulta Estatísticas-------------------------------------------------------
if df is not None:
    print("\n--- Consulta Estatística ---")
    
    while True:
        print("\nColunas disponíveis:")
        colunas_numericas = df.select_dtypes(include=['number']).columns
        for col in colunas_numericas:
            print(f" - {col}")

        coluna = input("Digite o nome da coluna para análise estatística (ou 999 para seguir em frente): ")

        if coluna == "999":
            print("Encerrando análise estatística...")
            break

        if coluna not in df.columns:
            print("Coluna não encontrada.")
            logging.warning(f"{nome_usuario} tentou acessar coluna inexistente: {coluna}")
        elif not pd.api.types.is_numeric_dtype(df[coluna]):
            print("A coluna não contém dados numéricos.")
            logging.warning(f"{nome_usuario} tentou acessar coluna não numérica: {coluna}")
        else:
            print(f"\nEstatísticas para '{coluna}':")
            print(f"Média: {df[coluna].mean():.2f}")
            print(f"Mediana: {df[coluna].median():.2f}")
            print(f"Moda: {df[coluna].mode().values[0]:.2f}")
            print(f"Desvio padrão: {df[coluna].std():.2f}")

            logging.info(f"{nome_usuario} visualizou estatísticas da coluna {coluna}.")


#-------------------------------Gera Gráficos--------------------------------------------------------------
if df is not None:
    print("\n--- Gerando Gráficos ---")

    if 'Sleep_Hours_per_Night' in df.columns and 'Final_Score' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x='Sleep_Hours_per_Night', y='Final_Score')
        plt.title("Horas de Sono x Nota Final")
        plt.xlabel("Horas de Sono")
        plt.ylabel("Nota Final")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("Colunas 'sleep_hours' e/ou 'final_score' não encontradas para gráfico de dispersão.")

    if 'Age' in df.columns and 'Midterm_Score' in df.columns:
        plt.figure(figsize=(8, 6))
        idade_media = df.groupby('Age')['Midterm_Score'].mean()
        idade_media.plot(kind='bar', color='skyblue')
        plt.title("Idade x Média das Notas Intermediárias")
        plt.xlabel("Idade")
        plt.ylabel("Média das Notas")
        plt.tight_layout()
        plt.show()
    else:
        print("Colunas 'age' e/ou 'midterm_score' não encontradas para gráfico de barras.")

    if 'Age' in df.columns:
        bins = [0, 17, 21, 24, 150]
        labels = ['Até 17', '18 a 21', '22 a 24', '25 ou mais']
        df['faixa_etaria'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)
        faixa_counts = df['faixa_etaria'].value_counts().sort_index()
        plt.figure(figsize=(6, 6))
        faixa_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title("Distribuição por Faixas Etárias")
        plt.ylabel('')
        plt.tight_layout()
        plt.show()
    else:
        print("Coluna 'age' não encontrada para gráfico de pizza.")

    logging.info(f"{nome_usuario} gerou os gráficos.")

