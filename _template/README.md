# Lab NN: <título curto>

## Pergunta

O que exatamente você quer descobrir. Uma pergunta específica e respondível,
não um tema. "Parquet é mais rápido?" é vago; "quanto tempo a menos leva para
ler 1 milhão de linhas em Parquet comparado a CSV?" é respondível.

## Contexto

Por que essa pergunta importa. Idealmente, uma decisão real que depende da
resposta — de preferência algo do projeto principal.

## Hipótese

O que você espera encontrar, **antes** de rodar o experimento.

Registre isso honestamente e não edite depois. Uma hipótese que se mostra errada
é o resultado mais valioso de um experimento — significa que você aprendeu algo
que não sabia.

## Método

Como o experimento foi montado:

- Qual dataset, qual tamanho, como foi gerado
- O que exatamente foi medido e como
- Quantas repetições (uma medição única é ruído, não resultado)
- Ambiente: máquina, versões das bibliotecas

Detalhe suficiente para alguém reproduzir.

## Resultado

Os números. Tabelas, gráficos, saída bruta.

Apresente o que foi observado antes de interpretar — separar o dado da
interpretação evita que a conclusão contamine a leitura.

## Conclusão

O que os números dizem, e o que isso muda na prática.

Inclua também os limites do experimento: em que condições esse resultado
provavelmente não se aplica. Um resultado obtido com 100 mil linhas não
necessariamente vale para 100 milhões.

## Aplicação no projeto principal

Se esta conclusão sustentou alguma decisão no Cadence Analytics, referencie o
ADR ou o trecho de código correspondente.

## Referências

Documentação e artigos consultados.
