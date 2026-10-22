# Squad MOD-1 — Fábrica de Modelos (B5) e Detecção por Quadro (I1)
**Disciplina:** Oficina de Desenvolvimento de Software (ODS 2026/2 — UFSJ)  
**Especificação:** Interfaces 1.0 (Arquitetura 6c Oficial)  
**Integrantes:** Felipe Girardi Siqueira (Líder), Thiago Mateus de Almeida Dias Orsini, Eduardo Monteiro Costa Pires

---

## 1. Estrutura do Repositório

```text
.
├── B5/
│   ├── tools/
│   │   ├── train_pipeline.py        # Treino automatizado + chamada ao empacotador
│   │   ├── package_artifact.py      # Exportação ONNX + geração dos 5 JSONs oficiais
│   │   ├── evaluate_quantization.py # Laudo técnico FP32 vs FP16 vs INT8 (T13)
│   │   └── remap_labels.py          # Utilitário de remapeamento de classes YOLO
│   └── artifacts/
│       ├── app-epi/1.0.0/           # Pacote MODEL Aplicação 1 (EPIs: pessoa, capacete, colete)
│       └── app-plates/1.0.0/        # Pacote MODEL Aplicação 2 (VER-5: 4 classes de placas)
├── I1/
│   ├── detector/
│   │   ├── config.py                # AppConfig e leitura automática de metadados de B5
│   │   ├── contracts.py             # Envelope EV-SINAL, ods.p4.frame e exceções de P2
│   │   ├── ingestion.py             # Conversão dinâmica BGR, RGB, GRAY e NV12
│   │   ├── inference.py             # Cliente da API fechada P2 (load, infer, info, release)
│   │   ├── postprocessing.py        # Filtro de confiança, NMS por classe e bbox inteira
│   │   ├── publishing.py            # Validador B1 acoplado, deduplicação UUIDv4, Stdout/Kafka
│   │   └── pipeline.py              # Orquestrador, controle de sessão (B2) e telemetria
│   ├── tests/
│   │   └── test_i1_sprint3.py       # Suíte automatizada de auditoria e contrato (T15)
│   ├── mock_producer.py             # Gerador de eventos sintéticos para CI (B4) e consumidores
│   └── run_detector.py              # CLI principal para execução do pipeline I1
├── schemas/
│   └── ods.i1.detections.v1.0.schema.json # Contrato formal JSON Schema (Draft 2020-12)
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
├── HOW_TO_RUN.md                    # Instruções sobre como executar o componente
└── STATUS_SPRINT3.md                # Relatório de acompanhamento das 21 tarefas da Sprint 3
```