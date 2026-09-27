import os
import math
import shutil
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.signal import savgol_filter, find_peaks

# +---------------+
# | Configurações |
# +---------------+

# Extensão de arquivos tratados
TIPO_CSV = ".csv"
TIPO_PNG = ".png"

# Pastas
PASTA_ARQUIVOS = "Gestos"
PASTA_COLETADOS = f"{PASTA_ARQUIVOS}\\coletados\\"
PASTA_BASE_DADOS = f"{PASTA_ARQUIVOS}\\base_dados\\"
PASTA_SEGMENTADOS = f"{PASTA_ARQUIVOS}\\segmentados\\"

# Classes dos gestos coletados
CLASSES = ["esquerda", "direita", "cima"]

# Número estimado de gestos coletados por tipo
NUM_GESTOS = 30

# Aproximadamente 476 Hz nos arquivos coletados
FREQUENCIA_AMOSTRAGEM = 476.0

# Janela usada para suavização
JANELA_SUAVIZACAO = 401

# Distância mínima entre dois gestos.
# Aproximadamente 2.65 segundos para obter 30 gestos.
DISTANCIA_MINIMA_SEGUNDOS = 2.65

# +---------+
# | Leitura |
# +---------+
def carregar_dados(nome_arquivo):

    df = pd.read_csv(nome_arquivo, sep=";")
    df = df.dropna()

    print(f"\n–––––– Arquivo: {nome_arquivo} ––––––")
    print(f"Nº de amostras: {len(df)}")

    tempo = df["Tempo giroscópio (s)"]

    print(f"Tempo inicial: {tempo.iloc[0]:.3f} s")
    print(f"Tempo final:   {tempo.iloc[-1]:.3f} s")
    print(f"Duração:       {tempo.iloc[-1] - tempo.iloc[0]:.3f} s")

    return df

# +-------------------------+
# | Magnitude do Giroscópio |
# +-------------------------+
def calcular_magnitude_giroscopio(df):
    gx = df["Giroscópio X (rad/s)"].values
    gy = df["Giroscópio Y (rad/s)"].values
    gz = df["Giroscópio Z (rad/s)"].values
    magnitude = np.sqrt(gx**2 + gy**2 + gz**2)
    return magnitude

# +---------------------+
# | Detecção dos gestos |
# +---------------------+
def detectar_gestos(df):

    magnitude = calcular_magnitude_giroscopio(df)
    magnitude = [x for x in magnitude if not (isinstance(x, float) and math.isnan(x))]

    # Suavização
    magnitude_suave = savgol_filter(
        magnitude,
        window_length=JANELA_SUAVIZACAO,
        polyorder=2
    )

    # Distância mínima entre dois picos
    distancia = int(DISTANCIA_MINIMA_SEGUNDOS * FREQUENCIA_AMOSTRAGEM)

    # Detecta os picos
    picos, propriedades = find_peaks(
        magnitude_suave,
        distance=distancia,
        prominence=0.2
    )

    print(f"\nPicos encontrados: {len(picos)}.")

    for i, pico in enumerate(picos):
        tempo = df["Tempo giroscópio (s)"].iloc[pico]
        print(
            f"Gesto {i + 1:02d}: "
            f"amostra = {pico:5d}; "
            f"tempo = {tempo:8.3f}s."
        )

    return magnitude, magnitude_suave, picos

# +-------------------------------+
# | Cria os segmentos de um gesto |
# +-------------------------------+
def criar_segmentos(df, picos):

    segmentos = []

    for i in range(len(picos)):

        centro = picos[i]

        # Primeiro gesto
        if i == 0:
            distancia_anterior = (picos[i + 1] - picos[i])
            inicio = max(0, centro - distancia_anterior // 2)
        else:
            inicio = (picos[i - 1] + picos[i]) // 2

        # Último gesto
        if i == len(picos) - 1:
            distancia_posterior = (picos[i] - picos[i - 1])
            fim = min(len(df), centro + distancia_posterior // 2)
        else:
            fim = (picos[i] + picos[i + 1]) // 2

        segmento = df.iloc[inicio:fim].copy()
        segmento["gesto"] = i + 1
        segmentos.append(segmento)

    return segmentos

# +-------------------------------------------------+
# | Mostra e salva o gráfico dos sinais de um gesto |
# +-------------------------------------------------+
def plotar_salvar_gesto_detectado(df, magnitude, magnitude_suave, picos, nome_classe, nome_arquivo):

    tempo = df["Tempo giroscópio (s)"].values

    plt.figure(figsize=(16, 6))

    plt.plot(
        tempo,
        magnitude,
        alpha=0.25,
        label="Magnitude original"
    )

    plt.plot(
        tempo,
        magnitude_suave,
        label="Magnitude suavizada"
    )

    plt.scatter(
        tempo[picos],
        magnitude_suave[picos],
        marker="o",
        label="Gestos detectados"
    )

    plt.xlabel("Tempo (s)")
    plt.ylabel("Magnitude do giroscópio (rad/s)")
    plt.title(f"Detecção de Gesto — {nome_classe.capitalize()} ({nome_arquivo})")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    nome_imagem = (f"{PASTA_BASE_DADOS}Gesto_{nome_arquivo}{TIPO_PNG}")

    plt.savefig(nome_imagem, dpi=150)
    # plt.show()

# +---------------------------------------------------------+
# | Gera o arquivo de segmentos de cada gesto de uma classe |
# +---------------------------------------------------------+
def gerar_arquivo_segmentos(segmentos, nome_classe):

    pasta_classe = f"{PASTA_SEGMENTADOS}\\{nome_classe}"

    if not os.path.exists(pasta_classe):
        os.mkdir(pasta_classe)

    ordem = 1
    
    for indice, segmento in enumerate(segmentos):
        nome_arquivo = (f"{pasta_classe}\\{nome_classe}_{ordem:02d}{TIPO_CSV}")
        while os.path.exists(nome_arquivo):
            ordem += 1
            nome_arquivo = (f"{pasta_classe}\\{nome_classe}_{ordem:02d}{TIPO_CSV}")
        segmento.to_csv(nome_arquivo, sep=";", index=False)
        ordem += 1

    print(
        f"\n{len(segmentos)} segmentos salvos "
        f"para a classe '{nome_classe}'."
    )

def limpar_pasta(pasta_raiz):
    for pasta in Path(pasta_raiz).iterdir():
        if pasta.is_file():
            pasta.unlink()
        elif pasta.is_dir():
            limpar_pasta(pasta)

# +--------------------+
# | Programa Principal |
# +--------------------+
def main():

    limpar_pasta(PASTA_BASE_DADOS)
    limpar_pasta(PASTA_SEGMENTADOS)

    for nome_classe in CLASSES:

        nome_pasta_classe = f"{PASTA_COLETADOS}{nome_classe}"
        pasta_arquivos_coletados_classe = Path(nome_pasta_classe)

        for arquivo_coletado_classe in list(pasta_arquivos_coletados_classe.glob(f'*{TIPO_CSV}')):

            df = carregar_dados(arquivo_coletado_classe)
            (magnitude, magnitude_suave, picos) = detectar_gestos(df)

            # Adverte caso o número de gestos esperados não tenha sido atingido
            if len(picos) != NUM_GESTOS:
                print(
                    f"\n---> Eram esperados {NUM_GESTOS} gestos, "
                    f"mas foram detectados {len(picos)}."
                )

            # Cria os segmentos
            segmentos = criar_segmentos(df, picos)

            # Grava o arquivo de segmentos do gesto corrente
            gerar_arquivo_segmentos(segmentos, nome_classe)

            # Gráfico
            plotar_salvar_gesto_detectado(
                df,
                magnitude,
                magnitude_suave,
                picos,
                nome_classe,
                pathlib.Path(arquivo_coletado_classe).stem
            )

if __name__ == "__main__":
    main()