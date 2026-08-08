# Lab 01: Formatos de arquivo — CSV, JSON e Parquet

## Pergunta

Para o mesmo conjunto de dados, quanto muda o **tamanho em disco** e o **tempo
de leitura** entre CSV, JSON e Parquet? E o ganho do Parquet se mantém quando a
consulta lê apenas algumas colunas?

## Contexto

O Cadence Analytics vai gravar dados brutos de métricas de saúde em uma camada
raw antes de processá-los. A escolha do formato afeta custo de armazenamento e
tempo de processamento de todo o pipeline a partir daí.

Parquet é o padrão recomendado em engenharia de dados, mas "é o padrão" não é
uma justificativa — vale medir a diferença no volume real deste projeto antes de
decidir.

## Hipótese

_(Preencher antes de rodar o experimento.)_

Espero que:

- Parquet produza o menor arquivo, seguido de CSV, com JSON sendo o maior — JSON
  repete o nome de cada campo em cada registro
- A diferença de tamanho seja de pelo menos 3x entre JSON e Parquet
- Parquet seja mais rápido de ler, mas a diferença seja pequena em volumes
  pequenos, já que o overhead de abrir o arquivo domina
- A vantagem do Parquet cresça bastante ao ler poucas colunas, por ser um
  formato colunar

## Método

_(Preencher conforme o experimento for montado.)_

**Dataset:** métricas diárias de saúde geradas sinteticamente, com colunas
numéricas e de texto — mesmo formato usado no Cadence Analytics.

**Volumes testados:** 10 mil, 100 mil e 1 milhão de linhas, para observar se o
comportamento muda com a escala.

**Medições:**

1. Tamanho do arquivo em disco, por formato e volume
2. Tempo de leitura completa do arquivo
3. Tempo de leitura de apenas 2 colunas

**Repetições:** cada medição de tempo repetida 5 vezes, registrando a mediana —
uma medição única sofre demais com cache de disco e variação do sistema.

**Ambiente:** _(preencher: SO, versão do Python, versões das bibliotecas)_

## Resultado

_(Preencher após rodar.)_

### Tamanho em disco

| Linhas | CSV | JSON | Parquet |
|--------|-----|------|---------|
| 10.000 | | | |
| 100.000 | | | |
| 1.000.000 | | | |

### Tempo de leitura completa (mediana de 5 execuções)

| Linhas | CSV | JSON | Parquet |
|--------|-----|------|---------|
| 10.000 | | | |
| 100.000 | | | |
| 1.000.000 | | | |

### Tempo de leitura de 2 colunas

| Linhas | CSV | JSON | Parquet |
|--------|-----|------|---------|
| 10.000 | | | |
| 100.000 | | | |
| 1.000.000 | | | |

## Conclusão

_(Preencher após analisar os resultados.)_

Pontos a responder:

- A hipótese se confirmou? Onde errei?
- Em que volume a diferença começa a importar de verdade?
- A leitura de poucas colunas mudou o quadro?
- Existe algum caso neste projeto em que CSV ou JSON ainda seria preferível?

**Limites deste experimento:** os volumes testados são pequenos comparados a
cenários reais de big data, e tudo roda em disco local — não em armazenamento de
objetos como S3, onde a latência de rede muda o cálculo. Os resultados indicam
tendência, não valores absolutos transferíveis.

## Aplicação no projeto principal

_(Preencher: referenciar o ADR do Cadence Analytics que documenta a escolha de
formato da camada raw.)_

## Referências

