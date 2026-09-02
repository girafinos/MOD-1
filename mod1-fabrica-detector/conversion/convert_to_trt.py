"""
Conversão e otimização: PyTorch -> ONNX -> TensorRT.

Uso:
    python convert_to_trt.py --run <run_id> --precision fp16|int8

Responsabilidades desta etapa (peso 3 em B5 — a mais incerta do componente):
- Exportar o modelo treinado para ONNX.
- Compilar para TensorRT na precisão escolhida.
- Medir o custo de acurácia da conversão com dados reais, não estimado.
- Registrar a latência medida na placa junto com o artefato publicado.
"""
import argparse
import json
from pathlib import Path


def convert(run_id: str, precision: str) -> dict:
    # TODO: exportação real para ONNX e compilação TensorRT.
    # Medir aqui a diferença de acurácia entre o modelo original e o convertido.
    result = {
        "run_id": run_id,
        "precision": precision,
        "onnx_path": f"registry/artifacts/{run_id}.onnx",
        "trt_path": f"registry/artifacts/{run_id}.trt",
        "latencia_ms_medida": None,
        "custo_acuracia": None,  # diferença de métrica vs. modelo original
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--precision", choices=["fp16", "int8"], default="fp16")
    args = parser.parse_args()

    result = convert(args.run, args.precision)
    out_path = Path("conversion") / f"conversion_{args.run}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Conversão registrada em {out_path}")
