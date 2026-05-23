from pydantic import BaseModel


class Detection(BaseModel):
    class_name: str
    confidence: float


class DetectionResponse(BaseModel):
    detections: list[Detection]
