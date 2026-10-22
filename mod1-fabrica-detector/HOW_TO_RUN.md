# Squad MOD-1 — Fábrica de Modelos (B5) e Detecção por Quadro (I1)

**Disciplina:** Oficina de Desenvolvimento de Software (ODS 2026/2 — UFSJ)  
**Especificação:** Interfaces 1.0 (Arquitetura 6c Oficial)  
**Integrantes:**
- Felipe Girardi Siqueira (Líder — Matrícula: 2023008120)
- Thiago Mateus de Almeida Dias Orsini (Matrícula: 2022004959)
- Eduardo Monteiro Costa Pires (Matrícula: 212050024)

---

## 1. Visão Geral e Arquitetura (Versão 6c)

O repositório do squad **MOD-1** concentra duas entregas centrais da Arquitetura 6c:

1. **Frente Transversal B5 (`B5/`):** Ferramental padronizado de preparação de dados, treinamento (`YOLOv8`), avaliação em partição de teste estritamente disjunta (`test`), análise comparativa de precisão/desempenho (`FP32`, `FP16`, `INT8`) e empacotamento imutável de modelos `ONNX` acompanhados dos 5 artefatos JSON oficiais (`manifest.json`, `run.json`, `metadata.json`, `descriptor.json` e `ods_artifact_published.json`).
2. **Componente I1 (`I1/` — Camada 2):** Detector de objetos por quadro projetado sob o princípio **"Um artefato por aplicação, um componente só"**. O código-fonte é único e agnóstico de domínio: a adaptação para diferentes aplicações (como detecção de EPIs ou detecção de Placas Veiculares) ocorre exclusivamente pela substituição do artefato `MODEL` (`.onnx` + `metadata.json`).

### Estrutura de Diretórios

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
└── STATUS_SPRINT3.md                # Relatório de acompanhamento das 21 tarefas da Sprint 3
```

---

## 2. Guia para Outros Squads: Execução via Docker

Não é necessário configurar ambiente Python localmente. Todos os fluxos de teste, simulação e inferência estão containerizados no `docker-compose.yaml`.

### 2.1. Para a Equipe de Testes e CI (B4 / TRA-2 — Tarefa T15)
Executa a suíte de auditoria `I1/tests/test_i1_sprint3.py`, validando:
- Aderência estrita ao envelope **EV-SINAL** (`ods.i1.detections` v1.0) e rejeição de campos legados;
- Emissão de `"detections": []` em quadros vazios e bloqueio de duplicatas por `message_id` (UUID v4);
- Pré-processamento dinâmico (`BGR`, `RGB`, `GRAY`, `NV12`) e NMS agrupado por classe;
- Tratamento dos 5 códigos de erro formais da biblioteca `P2`;
- Reinício determinístico de `sequence = 0` em eventos `START`, `SEEK`, `LOOP` e `RESTART` (**T6**);
- Supressão de quadro corrompido com log `[B2-OBS]` e lacuna implícita em `sequence` (**T7**);
- Execução fim a fim do **Degrau A** com o modelo ONNX real (**T16**).

```bash
docker compose run --rm i1-ci-tests
```

### 2.2. Para Consumidores (I2, I8, I9, S1) e B4: Produtor Mock (`mock_producer.py`)
Emite eventos sintéticos validados pelo validador acoplado de B1:

- **Modo `stdout` (imprime 10 eventos no terminal sem uso de rede):**
  ```bash
  docker compose run --rm i1-mock-stdout
  ```

- **Modo `kafka` (publica eventos no tópico `ods.i1.detections` do broker oficial `34.66.235.91:9093`):**
  ```bash
  docker compose run --rm i1-mock-kafka
  ```

- **Customizando a quantidade de quadros ou o endereço do broker Kafka:**
  ```bash
  ODS_KAFKA_BROKER=34.66.235.91:9093 docker compose run --rm i1-mock-kafka \
    python3 I1/mock_producer.py --frames 20 --mode kafka
  ```

### 2.3. Execução do Detector I1 com Modelos ONNX Reais (Degrau A — T16 e T20)
Comprova experimentalmente a propriedade **"Um artefato por aplicação, um componente só"**:

- **Aplicação 1 — Segurança / EPIs (`app-epi` v1.0.0: `pessoa`, `capacete`, `colete`):**
  ```bash
  docker compose run --rm i1-degrau-a
  ```

- **Aplicação 2 — Estacionamento / Placas (`app-plates` v1.0.0 — Squad VER-5):**
  ```bash
  docker compose run --rm i1-degrau-a \
    python3 I1/run_detector.py \
    --onnx /app/B5/artifacts/app-plates/1.0.0/app-plates.onnx \
    --metadata /app/B5/artifacts/app-plates/1.0.0/metadata.json \
    --source /app/B5/datasets/plates/global/test/images \
    --max-frames 10 \
    --conf 0.50 \
    --output-jsonl degrau_a_plates_events.jsonl
  ```

#### Parâmetros Suportados pelo `I1/run_detector.py`

| Parâmetro | Padrão | Descrição |
| :--- | :--- | :--- |
| `--onnx` | `B5/artifacts/app-epi/1.0.0/app-epi.onnx` | Caminho para o arquivo `.onnx` do pacote B5. |
| `--metadata` | `B5/artifacts/app-epi/1.0.0/metadata.json` | Caminho para o `metadata.json` (carrega `artifact_id`, `artifact_version` e `classes`). |
| `--source` | `"0"` | `0` para webcam, caminho de vídeo `.mp4` ou diretório de imagens de teste. |
| `--max-frames` | `20` | Limite de quadros a processar na sessão. |
| `--conf` | `0.50` | Limiar de confiança mínimo para manter detecções. |
| `--mode` | `"stdout"` | Destino de publicação: `stdout` (terminal) ou `kafka` (broker B3). |
| `--output-jsonl` | `"degrau_a_events.jsonl"` | Arquivo local onde os eventos validados são persistidos. |

---

## 3. Guia Interno (Squad MOD-1): Operação do Ferramental B5

Os scripts abaixo devem ser executados no ambiente local (`.venv` com suporte a GPU/CUDA) para treinar, empacotar e avaliar modelos:

### 3.1. Treinamento e Empacotamento Integrados (`train_pipeline.py`)
Executa o treinamento supervisionado, salva os pesos em `B5/runs/<artifact-id>/<version>/` e aciona automaticamente o `package_artifact.py` ao final:

```bash
python3 B5/tools/train_pipeline.py \
  --data B5/datasets/plates/global/data.yaml \
  --artifact-id app-plates \
  --artifact-version 1.0.0 \
  --dataset-id dataset-plates \
  --dataset-version 1.0.0 \
  --model yolov8s.pt \
  --epochs 50 \
  --patience 12 \
  --batch 16 \
  --origin "Dataset 20k Placas Balanceado (4 classes) - VER-5"
```

### 3.2. Empacotamento Standalone sem Retreinar (`package_artifact.py`)
Gera ou atualiza o arquivo `.onnx` (`opset=12`, `nms=False`, `simplify=True`) e os 5 arquivos JSON oficiais em `B5/artifacts/<artifact-id>/<version>/` a partir de um peso `best.pt` existente (lendo automaticamente o `args.yaml` do treino):

```bash
python3 B5/tools/package_artifact.py \
  --data B5/datasets/plates/global/data.yaml \
  --weights B5/runs/app-plates/1.0.0/weights/best.pt \
  --artifact-id app-plates \
  --artifact-version 1.0.0 \
  --dataset-id dataset-plates \
  --dataset-version 1.0.0 \
  --origin "Dataset 20k Placas Balanceado (4 classes) - VER-5"
```

### 3.3. Laudo de Acurácia e Desempenho por Precisão (`evaluate_quantization.py` — T13)
Avalia `FP32`, `FP16` e `INT8` na partição `test` isolada, aferindo `mAP@0.5`, `mAP@0.5:0.95`, `precision`, `recall`, tamanho em disco (MB), latência por quadro (ms), throughput (FPS) e pico de VRAM (MB). Gera `quantization_report.md` e `quantization_report.json` para subsidiar a compilação TensorRT pelo squad **SIS-1 (P2)**:

```bash
python3 B5/tools/evaluate_quantization.py \
  --data B5/datasets/plates/global/data.yaml \
  --weights B5/runs/app-plates/1.0.0/weights/best.pt \
  --artifact-id app-plates \
  --artifact-version 1.0.0 \
  --dataset-version 1.0.0
```

---

## 4. Contrato de Saída (`ods.i1.detections` v1.0 — Perfil EV-SINAL)

O schema formal em `schemas/ods.i1.detections.v1.0.schema.json` valida a estrutura abaixo em 100% das publicações de **I1**:

```json
{
  "message_type": "event",
  "message_id": "5f1e2c7a-9b1d-4e0a-8c6f-2d3a4b5c6d7e",
  "schema": "ods.i1.detections",
  "schema_version": "1.0",
  "producer": "I1",
  "published_at": "2026-10-21T14:30:00.120Z",
  "captured_at": "2026-10-21T14:29:59.870Z",
  "source_id": "cam0",
  "session_id": "9c2a1f3e-4d5b-4c6a-9e8f-0a1b2c3d4e5f",
  "sequence": 0,
  "artifact_version": "app-epi-1.0.0",
  "payload": {
    "frame_index": 0,
    "image_width": 1920,
    "image_height": 1080,
    "detections": [
      {
        "detection_id": 0,
        "class": "capacete",
        "confidence": 0.9312,
        "bbox": [412, 180, 598, 702]
      }
    ]
  }
}
```