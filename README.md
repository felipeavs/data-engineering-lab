# Data Engineering Lab

Experimentos curtos e isolados sobre conceitos de engenharia de dados.

Cada laboratório parte de uma **pergunta específica**, testa uma hipótese e
registra o que foi observado — com números, não impressões. O objetivo não é
reproduzir tutoriais, mas entender o comportamento real das ferramentas em
condições controladas.

Boa parte das conclusões aqui alimenta decisões técnicas do
[Cadence Analytics](https://github.com/felipeavs/cadence-analytics), meu projeto
principal de pipeline de dados.

## Estrutura

Cada laboratório é uma pasta independente, com seu próprio ambiente e README:

```
NN-nome-do-lab/
├── README.md          # pergunta, hipótese, método, resultado, conclusão
├── requirements.txt   # dependências isoladas
├── run.py             # o experimento
└── results/           # dados brutos e gráficos que sustentam a conclusão
```

## Laboratórios

| # | Tema | Pergunta | Status |
|---|------|----------|--------|
| 01 | Formatos de arquivo | CSV, JSON ou Parquet — quanto muda em tamanho e velocidade de leitura? | 🚧 Em andamento |
| 02 | Modelagem OLTP vs OLAP | A mesma informação em dois modelos: o que muda nas consultas analíticas? | ⏳ Planejado |
| 03 | Spark: particionamento | Como a estratégia de particionamento afeta o tempo de processamento? | ⏳ Planejado |
| 04 | Kafka: garantias de entrega | O que acontece com as mensagens quando o consumidor falha no meio do processamento? | ⏳ Planejado |
| 05 | Airflow: idempotência | Como construir uma DAG que pode ser reexecutada sem duplicar dados? | ⏳ Planejado |

## Como rodar

Cada laboratório é independente. Entre na pasta, instale as dependências e
execute:

```bash
cd 01-formatos-de-arquivo
pip install -r requirements.txt
python run.py
```

Alguns laboratórios exigem serviços auxiliares (Kafka, Postgres, Airflow). Nesses
casos há um `docker-compose.yml` na própria pasta do laboratório, e o README
explica como subir.
