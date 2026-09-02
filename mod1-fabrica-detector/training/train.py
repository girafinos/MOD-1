"""
Pipeline de treino genérico do B5.

Uso:
    python train.py --dataset <dataset_id> --config configs/<nome>.yaml

Responsabilidades desta etapa:
- Carregar o manifest do dataset (datasets/<dataset_id>/manifest.json).
- Treinar o modelo com a configuração dada.
- Avaliar com métrica adequada sobre um conjunto que não participou do treino.
- Gravar run.json com métricas, configuração e hash do dataset usado —
  é isso que alimenta o "registro e versionamento" exigido por B3.
"""
import argparse
import json
import datetime
from pathlib import Path


def load_manifest(dataset_id: str) -> dict:
    path = Path("datasets") / dataset_id / "manifest.json"
    with open(path) as f:
        return json.load(f)


def train(dataset_id: str, config_path: str) -> dict:
    manifest = load_manifest(dataset_id)

    # TODO: plugar aqui o framework de treino real (ex. Ultralytics YOLO).
    # A escolha de arquitetura é única para I1 — o que muda por aplicação
    # é o dataset e o class_map, não o código de treino.
    metrics = {
        "map50": None,
        "map50_95": None,
    }

    run = {
        "run_id": f"{dataset_id}-{datetime.date.today().isoformat()}",
        "dataset_id": dataset_id,
        "dataset_hash": manifest.get("hash_integridade"),
        "config": config_path,
        "metrics": metrics,
        "criado_em": datetime.datetime.utcnow().isoformat(),
    }
    return run


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    run = train(args.dataset, args.config)
    out_path = Path("training") / f"run_{run['run_id']}.json"
    with open(out_path, "w") as f:
        json.dump(run, f, indent=2)
    print(f"Run registrado em {out_path}")
