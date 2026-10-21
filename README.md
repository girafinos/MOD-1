# Squad MOD-1 — Fábrica de Modelos (B5) e Detecção por Quadro (I1)
**Disciplina:** Oficina de Desenvolvimento de Software (ODS 2026/2 — UFSJ)  
**Especificação:** Interfaces 1.0 (Arquitetura 6c Oficial)  
**Integrantes:** Felipe Girardi Siqueira (Líder), Thiago Mateus de Almeida Dias Orsini, Eduardo Monteiro Costa Pires

---

## 1. Estrutura do Repositório

```text
.
├── B5/
│   ├── tools/                  # Ferramental padronizado (treino, empacotamento, quantização)
│   └── artifacts/              # Registro imutável de pacotes MODEL e metadados oficiais
│       ├── app-epi/1.0.0/      # Artefato Aplicação 1 (EPIs: pessoa, capacete, colete)
│       └── app-parking/1.0.0/  # Artefato Aplicação 2 (VER-5 Estacionamento)
├── I1/
│   ├── detector/               # Código único do componente I1 (Camada 2)
│   │   ├── config.py           # AppConfig (leitura YAML + metadata.json do B5)
│   │   ├── contracts.py        # Envelope EV-SINAL, ods.p4.frame e exceções P2
│   │   ├── ingestion.py        # Pré-processamento dinâmico (BGR, RGB, GRAY, NV12)
│   │   ├── inference.py        # Cliente da API fechada de P2 (load, infer, info, release)
│   │   ├── postprocessing.py   # Filtro de confiança, NMS intra-classe e bbox inteira
│   │   ├── publishing.py       # Validador B1 pré-envio, deduplicação UUIDv4, Kafka/Stdout
│   │   └── pipeline.py         # Orquestrador, controle de sessão (B2) e telemetria
│   ├── tests/
│   │   └── test_i1_sprint3.py  # Suíte automatizada de contrato e integração (7 cenários)
│   ├── mock_producer.py        # Produtor sintético para CI de B4 e consumidores
│   └── run_detector.py         # Entrypoint de execução do pipeline I1
├── schemas/
│   └── ods.i1.detections.v1.0.schema.json # Contrato formal JSON Schema (Draft 2020-12)
├── Dockerfile
└── docker-compose.yaml