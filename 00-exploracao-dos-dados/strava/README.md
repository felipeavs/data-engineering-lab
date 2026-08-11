# Strava

Exploração dos dados disponíveis pela API do Strava.

## O que a API oferece

O Strava expõe **atividades** — cada corrida, pedalada ou treino registrado.
Não expõe métricas contínuas de saúde: sono, frequência cardíaca em repouso e
estresse não chegam ao Strava, mesmo que o dispositivo os colete.

Há dois níveis de detalhe, e a diferença entre eles é significativa.

### Atividade resumida

Retornada pelo endpoint de listagem. Cerca de 60 campos, quase todos escalares:

- **Identificação e contexto** — id, nome, tipo de esporte, data, cidade, se foi
  em rolo/esteira, equipamento usado
- **Métricas agregadas** — distância, tempo em movimento, tempo total, ganho de
  elevação, velocidade média e máxima
- **Esforço** — frequência cardíaca média e máxima, cadência, potência média,
  potência normalizada, quilojoules, suffer score
- **Social** — kudos, comentários, fotos, recordes pessoais batidos

Alguns campos aninhados aparecem mesmo aqui: `athlete` e `map` são objetos,
`start_latlng` e `end_latlng` são listas de coordenadas.

Uma requisição traz até 200 atividades.

### Atividade detalhada

Retornada pelo endpoint de atividade individual. Inclui tudo do resumo, mais as
estruturas realmente aninhadas:

- **`splits_metric`** — dados por quilômetro: tempo, ritmo, elevação e
  frequência cardíaca de cada trecho
- **`laps`** — voltas, quando o dispositivo as registrou
- **`segment_efforts`** — cada segmento percorrido, com tempo e classificação
- **`best_efforts`** — melhores tempos em distâncias padrão dentro da atividade
- **`calories`**, **`description`**, **`gear`**

O custo é uma requisição por atividade — bem diferente das poucas páginas que
trazem todos os resumos.

Essa diferença de estrutura é o que motivou o laboratório 01: dados aninhados
não sobrevivem a um CSV.

## Configuração

### 1. Registrar a aplicação

Em `strava.com/settings/api`, crie uma aplicação. O domínio de callback pode ser
`localhost` para desenvolvimento.

Anote o **Client ID** e o **Client Secret**.

### 2. Autorizar com o escopo correto

Este passo tem uma armadilha: o access token exibido na página da aplicação
**não serve** — ele não vem do fluxo OAuth e tem escopo insuficiente para ler
atividades.

É preciso autorizar explicitamente com `activity:read_all`. Abra no navegador,
substituindo o client id:

```
http://www.strava.com/oauth/authorize?client_id=SEU_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
```

Após autorizar, o navegador tentará abrir uma página no localhost e mostrará um
erro — isso é esperado. O que importa está na barra de endereço:

```
http://localhost/exchange_token?state=&code=ABC123&scope=read,activity:read_all
```

Confirme que `activity:read_all` aparece no `scope`. Copie o valor de `code`.

O `approval_prompt=force` é necessário: sem ele, o Strava reaproveita uma
autorização anterior, possivelmente com escopo antigo.

### 3. Trocar o código por tokens

O código de autorização vive poucos minutos e só pode ser usado uma vez. Faça um
POST para `https://www.strava.com/oauth/token` com os campos:

| Campo | Valor |
|-------|-------|
| `client_id` | o client id da aplicação |
| `client_secret` | o client secret |
| `code` | o código copiado do navegador |
| `grant_type` | `authorization_code` |

A resposta traz um `refresh_token` — é esse que você guarda.

### 4. Configurar o ambiente

No `.env` da raiz do repositório:

```
STRAVA_CLIENT_ID=...
STRAVA_CLIENT_SECRET=...
STRAVA_REFRESH_TOKEN=...
```

O access token **não** vai no `.env`: ele expira a cada seis horas e é obtido
automaticamente pelo cliente a partir do refresh token.

## Uso

```bash
pip install -r requirements.txt
python collect.py
```

A coleta é incremental e pode ser interrompida:

- **Atividades resumidas** — na primeira execução busca todo o histórico; nas
  seguintes, apenas o que veio depois da última atividade conhecida, com uma
  margem de sete dias para capturar atividades adicionadas com data retroativa
- **Detalhes** — cada atividade vira um arquivo próprio, e o conjunto de
  arquivos existentes funciona como cache. Rodar de novo busca apenas o que
  falta

Por padrão, `collect.py` busca 20 detalhes por execução. Ajuste o parâmetro
`limit` para buscar mais, ou passe `None` para buscar tudo.

## Estrutura dos dados

```
data/raw/
├── athlete.json           # perfil do atleta
├── activities.json        # lista completa de atividades resumidas
└── details/
    ├── 12345678.json      # uma atividade detalhada por arquivo
    └── ...
```

## Limites da API

O Strava limita requisições por janela de tempo — uma janela curta e um limite
diário. Ao estourar, a resposta é `429` e basta aguardar a janela reabrir; não
há bloqueio de conta nem penalidade.

A coleta usa uma pausa entre requisições e trata o `429` aguardando e tentando
novamente. Para o volume de uma conta pessoal, o limite dificilmente é atingido
— exceto ao reexecutar a coleta repetidamente durante o desenvolvimento, que é
justamente o cenário em que o cache ajuda.

Os valores atuais dos limites estão na documentação oficial e já mudaram ao
longo do tempo; vale conferir antes de assumir qualquer número.

## Observações

**O que não está aqui.** Sono, frequência cardíaca em repouso, estresse, HRV e
body battery não existem no Strava. Se o dispositivo Garmin estiver conectado,
as atividades chegam ao Strava automaticamente — mas as métricas diárias de
saúde, não.

**Campos condicionais.** Boa parte dos campos só é preenchida em certas
condições: potência exige medidor, frequência cardíaca exige cinta ou sensor
óptico, temperatura depende do dispositivo. Um inventário de valores nulos por
campo é o primeiro passo de qualquer análise aqui.

**Privacidade.** As atividades incluem coordenadas de início e fim. Os dados
coletados não são versionados, e qualquer resultado compartilhado usa dados
agregados.