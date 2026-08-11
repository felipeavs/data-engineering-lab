# Lab 01: Formatos de arquivo para a camada raw

## Pergunta

Para armazenar respostas da API do Strava em uma camada raw, qual formato —
CSV, JSON ou Parquet — oferece o melhor equilíbrio entre tamanho em disco,
velocidade de leitura e capacidade de representar dados aninhados?

Três medições respondem isso:

1. Quanto espaço cada formato ocupa para o mesmo conjunto de atividades?
2. Quanto tempo leva para ler o arquivo completo?
3. Quanto tempo leva para ler apenas alguns campos — e o formato colunar leva
   vantagem real aqui?

## Contexto

O [Cadence Analytics](https://github.com/felipeavs/cadence-analytics) ingere
dados de treino a partir da API do Strava (ver ADR003) e os armazena em uma
camada raw antes de qualquer transformação. A escolha do formato dessa camada
afeta custo de armazenamento e tempo de processamento de todo o pipeline daí em
diante.

Parquet é a recomendação padrão em engenharia de dados, mas "é o padrão" não é
justificativa. Além disso, há uma complicação específica a esta fonte: uma
atividade do Strava não é um registro plano. Ela contém campos aninhados —
splits, zonas de frequência cardíaca, dados do segmento — que os três formatos
tratam de maneiras bastante diferentes.

CSV não representa aninhamento de forma alguma: seria necessário achatar a
estrutura ou serializar os campos aninhados como texto. JSON representa
naturalmente. Parquet suporta tipos aninhados, mas ao custo de um schema mais
complexo.

Isso torna a comparação menos óbvia do que o benchmark genérico "Parquet é
melhor", e é exatamente por isso que vale medir.

## Hipótese

_(Preencher antes de rodar o experimento. Não editar depois.)_

Sobre tamanho:

- Parquet deve produzir o menor arquivo, por ser colunar e comprimido
- JSON deve ser o maior, já que repete o nome de cada campo em cada registro
- CSV deve ficar no meio — mas apenas porque os campos aninhados terão sido
  achatados ou serializados, o que já representa perda de informação estrutural

Sobre leitura:

- A diferença deve ser pequena em volumes baixos, onde o custo de abrir o
  arquivo domina
- A vantagem do Parquet deve crescer com o volume

Sobre leitura parcial:

- Aqui espero a maior diferença. Parquet deveria ler apenas as colunas
  solicitadas; CSV e JSON precisam percorrer o arquivo inteiro para descartar o
  que não foi pedido

Sobre aninhamento:

- Espero que CSV exija uma decisão de design (achatar ou serializar) que os
  outros dois não exigem, e que isso seja o fator mais decisivo — mais que
  qualquer diferença de tamanho ou velocidade

## Método

_(Preencher conforme o experimento for montado.)_

**Dataset:** atividades no formato retornado pela API do Strava, com os campos
aninhados preservados. Gerado sinteticamente a partir da estrutura de uma
resposta real, replicada com variação nos valores.

**Volumes testados:** 1 mil, 10 mil e 100 mil atividades. Os volumes são
menores que os do benchmark original porque cada registro é substancialmente
maior — uma atividade tem dezenas de campos, contra os poucos de uma métrica
diária.

**Medições:**

1. Tamanho do arquivo em disco, por formato e volume
2. Tempo de leitura completa
3. Tempo de leitura de 3 campos apenas (por exemplo: id, data, distância)
4. Registro qualitativo de como cada formato lidou com os campos aninhados

**Repetições:** cada medição de tempo repetida 5 vezes, registrando a mediana.
Uma medição única sofre demais com variação do sistema.

**Sobre cache de disco:** o sistema operacional mantém em memória arquivos lidos
recentemente, então a segunda leitura de um mesmo arquivo tende a ser mais
rápida que a primeira — independentemente do formato. As medições aqui são
feitas com cache quente (uma leitura descartada antes de iniciar as medições),
o que representa o cenário de leituras repetidas, não o de primeira leitura.

**Ambiente:** _(preencher: SO, versão do Python, versões das bibliotecas)_

## Resultado

_(Preencher após rodar.)_

### Tamanho em disco

| Atividades | CSV | JSON | Parquet |
|-----------|-----|------|---------|
| 1.000 | | | |
| 10.000 | | | |
| 100.000 | | | |

### Tempo de leitura completa (mediana de 5 execuções)

| Atividades | CSV | JSON | Parquet |
|-----------|-----|------|---------|
| 1.000 | | | |
| 10.000 | | | |
| 100.000 | | | |

### Tempo de leitura de 3 campos

| Atividades | CSV | JSON | Parquet |
|-----------|-----|------|---------|
| 1.000 | | | |
| 10.000 | | | |
| 100.000 | | | |

### Tratamento de campos aninhados

_(Registrar o que foi necessário fazer em cada formato, e o que se perdeu.)_

| Formato | Como representou | O que se perdeu |
|---------|------------------|-----------------|
| CSV | | |
| JSON | | |
| Parquet | | |

## Conclusão

_(Preencher após analisar os resultados.)_

Pontos a responder:

- A hipótese se confirmou? Onde errei?
- A partir de qual volume a diferença começa a importar de verdade?
- A leitura parcial mudou o quadro tanto quanto o esperado?
- O tratamento de aninhamento foi decisivo, ou tamanho e velocidade pesaram
  mais?
- Existe algum caso neste projeto em que CSV ou JSON ainda seria preferível?

**Limites deste experimento:** os volumes testados são pequenos comparados a
cenários reais de big data, e tudo roda em disco local — não em armazenamento de
objetos como S3, onde a latência de rede muda o cálculo e a capacidade de ler
apenas partes de um arquivo tem peso diferente. Os resultados indicam tendência,
não valores absolutos transferíveis.

Além disso, o dataset é sintético. Dados reais do Strava podem ter distribuições
de valores e proporções de campos nulos que afetam a compressão de forma
diferente.

## Aplicação no projeto principal

_(Preencher: referenciar o registro de decisão do Cadence Analytics que
documenta a escolha de formato da camada raw, uma vez escrito.)_

## Referências

_(Preencher com a documentação consultada.)_