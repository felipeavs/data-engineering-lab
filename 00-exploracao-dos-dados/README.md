# 00 — Exploração dos dados

Esta pasta reúne o trabalho de descobrir **o que existe** nas fontes de dados
antes de decidir o que fazer com elas.

Diferente dos laboratórios numerados a partir de 01, aqui não há hipótese a
testar nem medição a fazer. O objetivo é responder perguntas mais básicas: quais
campos cada API retorna, o que está preenchido de fato, qual a granularidade, e
que perguntas esses dados conseguem responder.

O resultado desta exploração alimenta duas coisas: as decisões de modelagem do
[Cadence Analytics](https://github.com/felipeavs/cadence-analytics) e os
datasets usados nos laboratórios seguintes.

## Fontes

| Fonte | Status | O que traz |
|-------|--------|------------|
| [Strava](./strava) | 🚧 Em andamento | Atividades: distância, ritmo, frequência cardíaca durante o exercício, potência, splits, segmentos |
| Garmin | ⏳ Planejado | Métricas diárias de saúde: sono, frequência cardíaca em repouso, estresse, HRV, passos |

As duas fontes são complementares e não se sobrepõem: o Strava cobre o lado do
**treino**, o Garmin cobre o lado da **recuperação**. A análise que motivou o
projeto — entender como carga de treino e recuperação se relacionam — depende
das duas.

A ordem não é arbitrária. O Strava tem API oficial com OAuth, então serve para
validar o pipeline de ingestão em condições previsíveis. O Garmin exige uma
biblioteca não oficial, com as ressalvas que isso implica, e entra depois que a
estrutura estiver funcionando. O raciocínio completo está registrado no ADR003
do projeto principal.

## O que se busca descobrir

Em cada fonte, as mesmas perguntas:

**Inventário.** Quais campos existem? Quais estão realmente preenchidos, e
quais só aparecem em certos tipos de atividade ou certos dispositivos?

**Granularidade.** O dado é por evento, por dia, ou por minuto? Uma resposta da
API corresponde a uma linha, ou traz estruturas aninhadas que precisam ser
desmembradas?

**Cobertura temporal.** De quando até quando? Há lacunas — períodos sem
registro, mudanças de dispositivo que alteraram quais campos são preenchidos?

**Potencial analítico.** Que perguntas esses dados conseguem responder, e quais
ficam fora de alcance?

## Estrutura

```
00-exploracao-dos-dados/
├── README.md
└── strava/
    ├── README.md          # como autenticar, coletar, e o que a API retorna
    ├── client.py          # cliente da API, com renovação automática de token
    ├── collect.py         # coleta incremental, com cache
    ├── analysis.ipynb     # inventário e primeiras observações
    └── data/raw/          # respostas da API, sem transformação (não versionado)
```

## Sobre os dados coletados

A pasta `data/` não é versionada. São dados pessoais de saúde e treino,
incluindo coordenadas geográficas de onde as atividades aconteceram — publicar
isso num repositório aberto exporia rotina e localização.

Qualquer resultado compartilhado aqui usa dados agregados ou anonimizados.

## Princípio da camada raw

As respostas da API são gravadas exatamente como chegam, em JSON, sem
transformação. Nenhum campo é descartado, renomeado ou convertido no momento da
coleta.

O motivo é prático: transformação é onde erros de interpretação acontecem, e
descobrir um erro depois de ter descartado o dado original significa recoletar
tudo. Com a resposta bruta preservada, basta reprocessar.

Isso também explica a escolha de JSON em vez de CSV. As respostas contêm campos
aninhados — objetos e listas — que o formato tabular não representa sem perda.
Converter para CSV na coleta já seria uma transformação, e uma que perde
informação.

O quanto essa escolha custa em espaço e velocidade de leitura é justamente o que
o laboratório 01 mede.