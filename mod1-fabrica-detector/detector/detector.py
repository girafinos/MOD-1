"""
I1 — Detecção por quadro.

Um único detector, parametrizado por artefato e mapa de classes.
Trocar de aplicação nunca deve exigir trocar este código — apenas
o model_path e o class_map carregados via registry/artifacts.json.
"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Detection:
    bbox: tuple  # (x1, y1, x2, y2)
    class_id: int
    confidence: float


class Detector:
    def __init__(self, model_path: str, class_map: Dict[int, str], conf_threshold: float = 0.5):
        self.model_path = model_path
        self.class_map = class_map
        self.conf_threshold = conf_threshold
        self._engine = None

    def load(self) -> None:
        # TODO: carregar o motor TensorRT publicado por B5 a partir de model_path.
        self._engine = object()  # placeholder

    def run(self, frame) -> List[Detection]:
        """
        Recebe um quadro (já corrigido de distorção por P4) e devolve
        uma lista de detecções no formato exigido pelo contrato com B1.
        Confiança abaixo de conf_threshold deve ser descartada aqui;
        confiança acima disso sempre é exposta, nunca arredondada para
        "sim/não" — quem decide o que fazer com a incerteza é S2.
        """
        if self._engine is None:
            raise RuntimeError("Detector não carregado — chame load() primeiro.")
        # TODO: inferência real.
        return []
