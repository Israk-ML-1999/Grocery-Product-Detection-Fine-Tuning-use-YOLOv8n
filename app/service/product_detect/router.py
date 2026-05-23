from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
import io
from .model import load_model

router = APIRouter(prefix="/api", tags=["detection"])

# Load model once at startup
model = load_model()


@router.post("/detect", summary="Detect objects in an image")
async def detect_objects(file: UploadFile = File(..., description="Image file (JPEG/PNG)")):
    """
    Accept an image file, run YOLOv8 detection, and return a list of detected
    classes with confidence scores (no bounding boxes).
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        # Convert to OpenCV BGR format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Run inference
        results = model(img_cv, conf=0.25)[0]  # confidence threshold 0.25

        # Build response
        detections = []
        if results.boxes is not None:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                confidence = round(float(box.conf[0]), 2)
                class_name = model.names[cls_id]
                detections.append({
                    "class": class_name,
                    "confidence": confidence
                })

        return JSONResponse(content={"detections": detections})

    except Exception as e:
        raise HTTPException(500, f"Detection failed: {str(e)}")


@router.get("/health", summary="Health check")
async def health():
    return {"status": "ok"}
