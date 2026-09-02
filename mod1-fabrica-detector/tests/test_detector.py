"""
Testa que o contrato de saída do detector (caixa, classe, confiança)
se mantém estável — é o esquema que quase toda a camada 3 consome.
"""
from detector.detector import Detector, Detection


def test_run_sem_carregar_levanta_erro():
    det = Detector(model_path="inexistente.trt", class_map={0: "capacete"})
    try:
        det.run(frame=None)
        assert False, "deveria levantar RuntimeError"
    except RuntimeError:
        pass


def test_deteccao_tem_campos_do_contrato():
    d = Detection(bbox=(0, 0, 10, 10), class_id=0, confidence=0.9)
    assert hasattr(d, "bbox")
    assert hasattr(d, "class_id")
    assert hasattr(d, "confidence")
