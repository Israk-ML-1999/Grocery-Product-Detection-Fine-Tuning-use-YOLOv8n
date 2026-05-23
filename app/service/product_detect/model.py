from ultralytics import YOLO
import os

MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "model/best.pt")


class YOLOModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = YOLO(MODEL_PATH)
        return cls._instance


def load_model():
    return YOLOModel.get_instance()
