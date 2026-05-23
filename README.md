# Grocery Product Detection API 🛒

This project is a FastAPI-based backend application that utilizes a fine-tuned YOLOv8 model for detecting grocery products in images. It accepts image uploads, processes them using PyTorch and OpenCV, and returns the detected objects along with their confidence scores.

## Features
- **FastAPI Backend**: Fast and robust API for handling image uploads.
- **YOLOv8 Integration**: Uses `ultralytics` for state-of-the-art object detection.
- **Dockerized Environment**: Fully containerized using Docker and Docker Compose for easy deployment.
- **Nginx Reverse Proxy**: Uses Nginx to proxy API requests securely.

## Prerequisites
To run this project easily, you will need:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## How to Run the Project 🚀

The simplest way to run this application is by using Docker Compose. It will build the FastAPI backend container and an Nginx reverse proxy.

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Israk-ML-1999/Grocery-Product-Detection-Fine-Tuning-use-YOLOv8n.git
   cd Grocery-Product-Detection-Fine-Tuning-use-YOLOv8n
   ```

2. **Build and start the containers**:
   ```bash
   docker compose up --build
   ```
   *(Add `-d` at the end to run it in detached mode in the background).*

3. **Access the application**:
   - The API will be accessible via Nginx at `http://localhost:8088`.
   - The interactive API documentation (Swagger UI) is at `http://localhost:8088/docs`.

To stop the containers, use:
```bash
docker compose down
```

## How the API Works ⚙️

The application exposes the following key endpoints:

### 1. Object Detection Endpoint
- **URL**: `/api/detect`
- **Method**: `POST`
- **Description**: Accepts an image file (JPEG/PNG) and returns a JSON response containing the detected grocery products and their confidence levels.
- **Input**: Form-Data with a key `file` containing the image.
- **Success Response** (`200 OK`):
  ```json
  {
    "detections": [
      {
        "class": "oil",
        "confidence": 0.95
      },
      {
        "class": "rice",
        "confidence": 0.88
      }
    ]
  }
  ```

#### Example Usage (cURL):
```bash
curl -X 'POST' \
  'http://localhost:8088/api/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.jpg;type=image/jpeg'
```

### 2. Health Check Endpoint
- **URL**: `/api/health`
- **Method**: `GET`
- **Description**: Simple health check to verify if the API is running correctly.
- **Success Response** (`200 OK`):
  ```json
  {
    "status": "ok"
  }
  ```

### 3. Interactive Documentation
FastAPI automatically generates an interactive UI where you can test the endpoints directly from your browser.
- Go to [http://localhost:8088/docs](http://localhost:8088/docs) to access the Swagger UI.
- You can upload an image directly through this interface and see the detection results instantly!

## Project Structure 📁
- `app/service/product_detect/router.py`: Contains the FastAPI routing and inference logic.
- `app/service/product_detect/model.py`: Manages the loading of the YOLOv8 model (`best.pt`).
- `app/service/product_detect/schema.py`: Defines the Pydantic schemas for data validation.
- `requirements.txt`: Python dependencies needed for the project.
- `Dockerfile` & `docker-compose.yml`: Configurations for containerizing the application.
