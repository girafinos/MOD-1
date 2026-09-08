# MOD-1 — Fábrica e Detecção

Esqueleto de projeto para os componentes **B5 (fábrica de artefatos)** e **I1 (detector genérico)**
do ODS 2026/2. Ver `docs/architecture.md` e `docs/component-doc.md` para o racional completo.

## Estrutura

```
mod1-fabrica-detector/
├── docs/                    # arquitetura, documento complementar, diagramas
├── annotation/guides/       # um guia de rotulagem por aplicação (A1, A5, A6, ...)
├── datasets/<id>/           # uma pasta por versão de dataset, com manifest.json
├── training/                # pipeline de treino genérico + configs por execução
├── conversion/               # conversão PyTorch -> ONNX -> TensorRT
├── registry/                 # registro de artefatos publicados (artifacts.json)
├── detector/                 # implementação de I1 (classe Detector única)
└── tests/                    # testes do contrato de saída do detector
```

## Fluxo básico

1. Aplicação entrega dados brutos + guia de rotulagem em `annotation/guides/<app>.md`.
2. Anotar e gerar `datasets/<id>/manifest.json`.
3. Rodar `training/train.py --dataset <id> --config training/configs/<nome>.yaml`.
4. Converter com `conversion/convert_to_trt.py --run <run_id>`.
5. Publicar e registrar em `registry/artifacts.json`.
6. `detector/detector.py` carrega o artefato publicado e expõe `run(frame) -> List[Detection]`.
