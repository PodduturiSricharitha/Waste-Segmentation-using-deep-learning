# Waste Segmentation using Deep Learning

This project implements an AI-driven waste detection and segmentation system using **YOLOv8** instance segmentation. The goal is to identify and classify waste materials to assist in proper recycling and disposal.

## 🔍 Project Overview

- ✅ Custom-trained YOLOv8 large-seg model
- ✅ 22-class annotated dataset (bounding boxes + polygon segmentation)
- ✅ Flask web interface to upload images and get predictions
- ✅ Rule-based NLP module for disposal instructions

## 🧠 Model Details

- **Architecture**: YOLOv8-Large (Segmentation variant)
- **Framework**: Ultralytics YOLOv8 (PyTorch)
- **Format**: `.pt` model (stored locally)
- **Classes**: 22 waste categories (e.g., PVC, PET, Organic, Metal)

## 🗃️ Dataset

- **Source**: Aggregated from Roboflow Waste Detection 2.0 + other datasets. you can view and cite the dataset at https://universe.roboflow.com/charitha-ppjnc/waste-detection-2-whu8d/dataset/1
- **Size**: 1311 annotated images
- **Annotations**: Mixed format — bounding boxes for some classes, polygon segmentation for others

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

## 🧩 Tech Stack

- **Python**
- **OpenCV**
- **Flask** (for UI)
- **Ultralytics YOLOv8**
- **Rule-based NLP** for instructions

---

## 🙋 Author

**Sricharitha Podduturi**  
👩‍🎓 *BVRIT Narsapur — Computer Science*  
📜 *IEEE ICONAT 2024 Paper Contributor*
