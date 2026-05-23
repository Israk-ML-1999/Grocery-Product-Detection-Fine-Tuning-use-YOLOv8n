from fastapi import FastAPI
from app.service.product_detect.router import router

app = FastAPI(
    title="Grocery Detection API",
    description="Detect grocery products in an image using YOLOv8",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
