# Projeto de Mineração de Séries Temporais
Projeto da Disciplina de Mineração de Dados do Curso de Especialização em IA e Ciência de Dados da **PUC-PR**.

## Objetivo:
Coleta via celular com o aplicativo [_phyphox_](https://phyphox.org/) para registro de movimentos para a esquerda, direita e cima e avaliação com algoritmos de classificação.

### Descrição das Pastas:

| **Pasta** | **Descrição** |
| --- | --- |
| *Gestos* | Pasta-raiz dos arquivos do experimento. |
| *Gestos\base_dados* | Pasta da base de dados gerada a partir dos exemplos obtidos e das imagens dos sinais de cada gesto detectado. |
| *Gestos\coletados* | Medições dos gestos do experimento registradas com o aplicativo [_phyphox_](https://phyphox.org/). |
| *Gestos\segmentados* | Arquivos dos gestos identificados. |
| *phyphox* | Pasta do arquivo de configuração do experimento no [_phyphox_](https://phyphox.org/) especificando o uso de acelerômetro e giroscópio para detecção dos gestos. |

### Descrição dos Arquivos:

| **Arquivo** | **Descrição** |
| --- | --- |
| *gerar_base_dados.py* | Código *Python* de criação da base de dados a partir dos gestos detectados por classe. |
| *segmentar_gestos.py* | Código *Python* de segmentação dos gestos de cada classe a partir dos exemplos coletados também por classe. |
| *requirements.txt* | Bibliotecas utilizadas nos códigos *Python*. |
| *gestos_3_classes.ipynb* | *Jupyter Notebook* de aplicação de algoritmos de classificação para previsão dos gestos do experitmento. |

### Ordem de execução dos códigos Python:
- *segmentar_gestos.py*;
- *gerar_base_dados.py*.





