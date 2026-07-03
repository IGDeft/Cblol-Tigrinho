# Draft LOL Predict

Simulador de draft (picks & bans) de League of Legends com sugestões de campeões geradas por Inteligência Artificial, treinada com dados reais de partidas profissionais (Oracle's Elixir, temporadas 2025 e 2026).

O usuário monta um confronto entre dois times, simula toda a fase de banimentos e escolhas do draft (incluindo modo *fearless*, com múltiplos jogos) e, a cada turno, pode pedir para a IA sugerir o próximo pick ou ban, ou deixar que a própria IA jogue contra ele.

## Como funciona

O projeto é dividido em três partes que conversam entre si:

- **Frontend** (`frontend/`) — Interface web em React + Vite onde o usuário escolhe os times e realiza o draft.
- **Backend** (`draft-lol/`) — API em Java com Spring Boot que recebe as requisições do frontend, valida os dados e repassa para o serviço de IA.
- **IA / API de dados** (`python/`) — API em Python com FastAPI responsável pela lógica do draft, pelas estatísticas dos times e pelo modelo de Machine Learning (Random Forest) que sugere picks e bans.

```
Frontend (React)  --->  Backend (Spring Boot, :8080)  --->  API Python (FastAPI, :5000)
```

## Tecnologias

**Frontend**
- React 19
- Vite

**Backend**
- Java 17
- Spring Boot 3.5
- Spring Cloud OpenFeign (comunicação com a API Python)
- Springdoc OpenAPI (documentação Swagger)
- Lombok

**IA / Dados**
- Python
- FastAPI + Uvicorn
- Pandas / NumPy
- scikit-learn (RandomForestClassifier)
- Base de dados: [Oracle's Elixir](https://oracleselixir.com/) (partidas de 2025 e 2026)

## Estrutura do repositório

```
Draft-LOL-Predict/
├── frontend/          # Aplicação React (interface do draft)
├── draft-lol/         # API Java/Spring Boot (orquestra as requisições)
└── python/            # API Python/FastAPI (IA e análise de dados)
    ├── api.py            # Endpoints da API
    ├── cblol.py          # Tratamento dos dados e modelo de IA
    ├── draft.py          # Máquina de estados das fases do draft
    └── *.csv              # Bases de partidas (Oracle's Elixir)
```

## Pré-requisitos

- [Node.js](https://nodejs.org/) 18+ e npm
- [Java 17](https://adoptium.net/)
- [Maven](https://maven.apache.org/) (ou use o `mvnw` incluso no projeto)
- [Python 3.10+](https://www.python.org/)

## Como rodar o projeto

O projeto precisa das três partes rodando ao mesmo tempo, cada uma em um terminal.

### 1. API Python (IA)

```bash
cd python
pip install fastapi uvicorn pandas numpy scikit-learn
python api.py
```

A API sobe em `http://localhost:5000`.

### 2. Backend Java (Spring Boot)

```bash
cd draft-lol
./mvnw spring-boot:run
```

A API sobe em `http://localhost:8080`. A documentação Swagger fica disponível em `http://localhost:8080/docs`.

### 3. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

A aplicação sobe em `http://localhost:5173`, endereço configurado como origem permitida (CORS) no backend.

## Principais endpoints (Backend Java)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/draft/champions` | Lista todos os campeões disponíveis |
| GET | `/draft/times` | Lista todos os times disponíveis |
| POST | `/draft/Start` | Inicia uma nova sessão de draft |
| POST | `/draft/Picks-Bans` | Registra um pick ou ban na sessão |
| POST | `/draft/Prox-jogo` | Avança para o próximo jogo (modo fearless) |
| GET | `/draft/Sugestao` | Pede à IA uma sugestão de pick/ban |
| GET | `/draft/sessao` | Consulta o estado atual de uma sessão |

## Como as sugestões são calculadas

Diferente do que o nome "IA" sugere, o modelo de Machine Learning é só uma peça do sistema. Cada sugestão de pick ou ban (`cblol.py`) é o resultado de uma **pontuação combinada (score)**, somando um motor de aprendizado por contexto com um motor puramente estatístico, calculado sobre o histórico de partidas. No pick, por exemplo, o peso do modelo de ML gira em torno de apenas 25% do score final — o resto vem das análises estatísticas descritas abaixo.

### 1. Motor de Machine Learning (aprendizado por contexto)

Um `RandomForestClassifier` (scikit-learn) treinado com o histórico de partidas profissionais de 2025/2026. Ele aprende o **contexto** de cada pick: dado o time, o adversário, a rota, a ordem do draft (first pick ou não), os campeões já escolhidos pelo próprio time e os já revelados do time adversário, o modelo estima a probabilidade de cada campeão ser escolhido naquela situação. Partidas de ligas mais fortes (LCK, LPL, MSI, EWC) e patches mais recentes recebem peso maior no treino (`peso_liga`, `patch_peso`), assim como a liga selecionada pelo usuário (`bonus_liga_ativa`).

### 2. Motor estatístico (regras sobre os dados históricos)

Calculado em tempo real a partir das tabelas de partidas, sem nenhum modelo treinado — são frequências, médias e taxas de vitória extraídas diretamente dos dados:

- **Prioridade histórica** — frequência com que cada time escolheu cada campeão (e, separadamente, sua prioridade no primeiro pick da partida).
- **Sinergia entre aliados** — com que frequência dois campeões já foram escolhidos juntos pelo mesmo time.
- **Força de counter** — winrate de um campeão contra outro em confrontos diretos (matchup), com limiar mínimo de exposição para considerar a amostra confiável.
- **Resposta a picks do adversário** — histórico de "respostas" que um time costuma dar depois que o rival escolhe determinado campeão.
- **Ameaça de ban** — probabilidade de o time sofrer ban de um campeão específico contra aquele adversário, usada para antecipar picks/bans oportunistas.
- **DNA de rota** — percentual histórico de vezes que cada campeão foi jogado em cada posição (top/jng/mid/bot/sup), usado para saber quais rotas do time já estão "ocupadas" e quais campeões realmente flexam de rota.

Esses dois motores são combinados em pesos que mudam ao longo do draft (por exemplo, o peso da sinergia e do counter aumenta conforme mais picks já foram feitos, enquanto o peso de "oportunidade" de ban diminui). No fim, os três melhores candidatos são sorteados de forma ponderada pelo score, o que evita que a IA seja sempre 100% previsível.

O modo *fearless* (múltiplos jogos na mesma série) também entra na conta: campeões já usados por qualquer um dos dois times em jogos anteriores da série ficam bloqueados nas rodadas seguintes.

## Status

Projeto em desenvolvimento.
