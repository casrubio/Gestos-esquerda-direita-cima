Experimento **phyphox** — Classificação de Gestos (3 classes)

**Classes:**
- movimento para a esquerda;
- movimento para a direita;
- movimento para cima.

**Coleta:**
- 30 repetições por classe;
- aproximadamente 0,5s parado + 1,0s executando o gesto + 0,5 s parado;
- pequena pausa entre as repetições;
- orientação do telefone mantida constante;
- movimentos de cada classe gravados em um arquivo CSV;
- 5 coletas × 3 classes × 30 repetições = 450 exemplos esperados.

**Sensores**:
- acelerômetro X/Y/Z + tempo (sensor bruto, incluindo gravidade);
- giroscópio X/Y/Z + tempo;
- *rate="0"* e *rateStrategy="request"* preservam a taxa real fornecida pelo dispositivo.

**Sequência:**<br>
Os CSVs são processados para verificar a taxa de amostragem, alinhar *timestamps*,<br>
detectar/segmentar as repetições e normalizar as janelas e formar X/y.
