import os
import numpy as np
import pandas as pd

# +--------------+
# | Configuração |
# +--------------+

PASTA_ARQUIVOS = "Gestos"
ARQUIVO_SAIDA = "gestos_3_classes.csv"
CLASSES = { "esquerda": 0, "direita": 1, "cima": 2 }

# +-----------------+
# | Características |
# +-----------------+
def calcular_caracteristicas(sinal):

    sinal = np.asarray(sinal, dtype=float)
    media = np.mean(sinal)
    desvio_padrao = np.std(sinal)
    minimo = np.min(sinal)
    maximo = np.max(sinal)
    amplitude = maximo - minimo
    rms = np.sqrt(np.mean(sinal ** 2))
    mediana = np.median(sinal)
    energia = np.sum(sinal ** 2)

    return {
        "media": media,
        "std": desvio_padrao,
        "min": minimo,
        "max": maximo,
        "amplitude": amplitude,
        # Root Mean Square (Raiz Quadrática Média) - Intensidade Média do Sinal
        "rms": rms,
        "mediana": mediana,
        # Intensidade Acumulada do Sinal
        "energia": energia
    }

# +-------------------+
# | Processa um Gesto |
# +-------------------+

def extrair_gesto(arquivo, numero_gesto, nome_classe, codigo_classe):

    # Carrega o arquivo corresponde aos movimento do gesto
    df = pd.read_csv(arquivo, sep=";")

    sinais = {
        "ax": "Acelerômetro X (m/s²)",
        "ay": "Acelerômetro Y (m/s²)",
        "az": "Acelerômetro Z (m/s²)",
        "gx": "Giroscópio X (rad/s)",
        "gy": "Giroscópio Y (rad/s)",
        "gz": "Giroscópio Z (rad/s)"
    }

    # Extrái as características de cada sinal
    caracteristicas = {}
    for sigla, nome_coluna in sinais.items():
        valores = df[nome_coluna].dropna().values
        estatisticas = calcular_caracteristicas(valores)
        for nome_estatistica, valor_estatistica in estatisticas.items():
            nome_caracteristica = f"{sigla}_{nome_estatistica}"
            caracteristicas[nome_caracteristica] = valor_estatistica

    # Informações do gesto
    caracteristicas["gesto"] = numero_gesto
    caracteristicas["classe"] = codigo_classe
    caracteristicas["nome_classe"] = nome_classe
    caracteristicas["duracao"] = (
        df["Tempo giroscópio (s)"].iloc[-1] -
        df["Tempo giroscópio (s)"].iloc[0]
    )

    caracteristicas["numero_amostras"] = len(df)
    return caracteristicas

# +----------------------+
# | Cria a base de dados |
# +----------------------+

def criar_base_dados():

    registros = []
    
    for nome_classe, codigo_classe in CLASSES.items():
        
        # Define o nome da pasta dos arquivos coletados para a classe
        pasta_segmentados_classe = os.path.join(
            PASTA_ARQUIVOS, f"segmentados\\{nome_classe}"
        )

        # Desconsidera caso a pasta inexista
        if not os.path.exists(pasta_segmentados_classe):
            print(f"A pasta \"{pasta_segmentados_classe}\" não foi encontrada!")
            continue

        # Obtém a lista de arquivos CSVs existentes na pasta da classe
        arquivos = sorted(
            arquivo
            for arquivo in os.listdir(pasta_segmentados_classe)
            if arquivo.endswith(".csv")
        )

        # Obtém as características de cada arquivo recuperado da pasta
        for numero, arquivo in enumerate(arquivos, start=1):
            arquivo_gesto = os.path.join(
                pasta_segmentados_classe,
                arquivo
            )
            caracteristicas = extrair_gesto(
                arquivo_gesto,
                numero,
                nome_classe,
                codigo_classe
            )
            registros.append(caracteristicas)

    # Carrega em um DataFrame os registros do arquivo processado
    base_dados = pd.DataFrame(registros)

    # Ordena o DataFrame por classe e gesto
    base_dados = base_dados.sort_values(["classe", "gesto"])

    # Salva a base de dados
    arquivo_saida = os.path.join(
        PASTA_ARQUIVOS,
        f"base_dados\\{ARQUIVO_SAIDA}"
    )
    
    base_dados.to_csv(arquivo_saida, sep=";", index=False)

    print("\n—————— Base de Dados Criada  ——————")
    print(f"Arquivo: {arquivo_saida}")
    print(f"Exemplos: {len(base_dados)}")
    print(f"Características: {len(base_dados.columns)} colunas")
    print(f"Números por classe:\n{base_dados["nome_classe"].value_counts()}")

    return base_dados

# +----------+
# | Execução |
# +----------+

if __name__ == "__main__":
    base_dados = criar_base_dados()
    print(base_dados.head(5))
