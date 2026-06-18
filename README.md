Name: R Dhaksesh

# AegisAI — Autonomous Disaster Intelligence Platform

```
User Query
    │
    ▼
[Agent 1] Incident Intake  ──► Kafka: incident-topic
    │
    ▼
[Agent 2] Situation Research (Qdrant RAG) ──► Kafka: research-topic
    │
    ├─────────────────────────────────┐
    ▼                                 ▼
[Agent 3] Infrastructure Risk   [Agent 4] Resource Discovery
  (Neo4j graph traversal)         (Qdrant + Neo4j hybrid)
    │                                 │
    └────────────┬────────────────────┘
                 ▼
        [Agent 5] Knowledge Graph (GraphRAG)
                 │
                 ▼
        [Agent 6] Strategy Planning (CoT)
                 │
                 ▼
        [Agent 7] Verification
                 │
                 ▼
        [Agent 8] Report Generation ──► Final Report
```

## Stack
| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph |
| LLM | GPT-4o / Claude |
| Vector DB | Qdrant |
| Graph DB | Neo4j |
| Message Bus | Apache Kafka |
| API | FastAPI |
| Frontend | React + Tailwind |
| Observability | LangSmith |
| Deployment | Docker Compose |

## Quick Start

```bash
cp .env.example .env
# Fill in API keys

docker compose up -d
python scripts/seed_data.py   # seed Qdrant + Neo4j

# API: http://localhost:8000
# UI:  http://localhost:3000
# Neo4j Browser: http://localhost:7474
```

## API

```
POST   /api/v1/incidents          { "query": "Flood in Chennai..." }
GET    /api/v1/incidents/{id}     Get incident status + state
WS     /api/v1/incidents/{id}/stream  Real-time agent updates
GET    /api/v1/reports/{id}       Final report
POST   /api/v1/reports/ingest     Upload PDF / text to Qdrant
```

## Agents

| # | Agent | Tools |
|---|-------|-------|
| 1 | Incident Intake | LLM classification |
| 2 | Situation Research | Qdrant (Agentic RAG) |
| 3 | Infrastructure Risk | Neo4j graph traversal |
| 4 | Resource Discovery | Qdrant + Neo4j hybrid |
| 5 | Knowledge Graph | GraphRAG |
| 6 | Strategy Planning | Chain-of-Thought LLM |
| 7 | Verification | Fact-check LLM |
| 8 | Report Generation | Structured output LLM |
