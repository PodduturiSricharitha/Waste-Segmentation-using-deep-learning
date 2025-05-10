# Waste Segmentation using Deep Learning

This project implements an AI-driven waste detection and segmentation system using **YOLOv8** instance segmentation. The goal is to identify and classify waste materials to assist in proper recycling and disposal.

## 🔍 Project Overview

- ✅ Custom-trained YOLOv8 large-seg model
- ✅ 22-class annotated dataset (bounding boxes + polygon segmentation)
- ✅ Flask web interface to upload images and get predictions
- ✅ Rule-based NLP module for disposal instructions

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/PodduturiSricharitha/Waste-Segmentation-using-deep-learning.git
   cd Waste-Segmentation-using-deep-learning
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
   ```bash
   python app.py

🧠 Model
Architecture: YOLOv8 Large Instance Segmentation

Training: Custom dataset from Roboflow (22 classes)

Format: Trained with .pt weights (stored externally)

🗃️ Dataset
Source: Roboflow Waste Detection 2.0 (https://universe.roboflow.com/charitha-ppjnc/waste-detection-2-whu8d/dataset/1)
You can cite the dataset from above link
Includes real-world mixed-material and recyclable waste images

📦 Tech Stack
Python

OpenCV, Ultralytics YOLOv8

Flask

Rule-based NLP

Jinja2 for templating

👩‍💻 Author
Sricharitha Podduturi
BVRIT Narsapur | CSE Department
IEEE ICONAT 2024 paper contributor
