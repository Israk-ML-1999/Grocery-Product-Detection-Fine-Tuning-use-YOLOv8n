# Grocery Product Detection API 🛒

This project is a FastAPI-based backend application that utilizes a fine-tuned **YOLOv8n** model for detecting grocery products in images. It accepts image uploads, processes them using PyTorch and OpenCV, and returns the detected objects along with their confidence scores.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)


## Features
- **FastAPI Backend**: Fast and robust API for handling image uploads.
- **YOLOv8 Integration**: Uses `ultralytics` for state-of-the-art object detection.
- **Dockerized Environment**: Fully containerized using Docker and Docker Compose for easy deployment.
- **Nginx Reverse Proxy**: Uses Nginx to proxy API requests securely.

---

## 🧠 Model Performance & Training Details

### Dataset
- **Source**: [Roboflow Universe – Grocery ey3gm](https://universe.roboflow.com/product5k/grocery-ey3gm)
- **Classes**: 25 (beans, cake, candy, cereal, chips, chocolate, coffee, corn, fish, flour, honey, jam, juice, milk, nuts, oil, pasta, rice, soda, spices, sugar, tea, tomato_sauce, vinegar, water)
- **Image resolution**: 416×416 pixels (all images resized to this square format)
- **Dataset size**: ~5000 images total → only ~200 images per class on average (small dataset)

### Training Environment & Constraints
- **Platform**: Kaggle (free GPU – Tesla T4/P100)
- **GPU memory limit**: 15 GB → batch size limited to 16
- **Epochs**: 25 (due to free usage quotas; optimal performance would require >100 epochs)
- **Image size**: 416×416 (native resolution used, no upscaling)
- **Loss functions**: box loss, class loss, DFL loss (YOLOv8 default)
- **Data augmentation**: mosaic, mixup, fliplr, HSV shifts (default YOLOv8 settings)

### Achieved Metrics (on validation set)
| Metric            | Value   |
|-------------------|---------|
| **mAP50**         | 0.8494  |
| **mAP50‑95**      | 0.7135  |
| **Precision**     | 0.8011  |
| **Recall**        | 0.7758  |

> **Note**: These results were obtained after **only 25 epochs** on a small dataset. With more epochs and a larger, balanced dataset, performance would improve significantly.

---

## 🚧 Limitations & Improvement Opportunities

### Current Limitations
1. **Small per‑class dataset** – only ~200 images per category → limits generalisation.
2. **Low number of epochs** (25) – the model has not fully converged.
3. **Free GPU constraints** – prevented training with larger batch sizes, higher resolution (e.g., 640×640), or longer training.
4. **Fixed 416×416 input** – some fine details (e.g., small text on labels) may be lost compared to 640×640.

### How to Achieve Better Results
- ✅ **Increase epochs to 100–150** – the loss curves were still decreasing at epoch 25.
- ✅ **Use a higher input resolution** (e.g., 640×640) if GPU memory allows (requires batch size reduction).
- ✅ **Collect more data** – at least 500–1000 images per class.
- ✅ **Apply stronger augmentation** – especially for small objects/text regions.
- ✅ **Use a larger YOLO variant** (YOLOv8s, YOLOv8m) if compute permits.

---

## 🚀 How to Run the Project

The simplest way to run this application is by using Docker Compose. It will build the FastAPI backend container and an Nginx reverse proxy.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Israk-ML-1999/Grocery-Product-Detection-Fine-Tuning-use-YOLOv8n.git
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

---

## How the API Works

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

---

## 📁 Project Structure
```text
.
├── app/
│   └── service/
│       └── product_detect/
│           ├── model.py       
│           ├── router.py      
│           └── schema.py      
├── nginx/
│   └── nginx.conf             
├── Dockerfile                 
├── docker-compose.yml
├── main.py        
└── requirements.txt
```
