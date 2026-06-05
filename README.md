# Computer Vision & Deep Learning: Modelos Avanzados de Clasificación y Detección de Objetos

## 📊 Vista General del Proyecto
Este proyecto de Inteligencia Artificial ha sido desarrollado en el marco del Bootcamp de Data Analytics & AI en Upgrade Hub. Su objetivo principal es el diseño, entrenamiento y evaluación de modelos basados en **Redes Neuronales** para la resolución de problemas complejos de análisis predictivo, clasificación de imágenes y detección de objetos en tiempo real. 

El repositorio combina dos de los enfoques más robustos en el ecosistema actual de IA:
1. **Deep Learning Clásico (TensorFlow/Keras):** Para el modelado predictivo y extracción de patrones de datos estructurados/no estructurados mediante Redes Neuronales Artificiales (ANN) y Convolucionales (CNN).
2. **Visión Artificial del Estado del Arte (Ultralytics/YOLO):** Para la localización y detección automatizada de objetos, una tecnología con alto impacto directo en sectores como la automatización industrial, control de calidad, seguridad y optimización de operaciones (InsurTech/Smart Cities).

---

## 🛠️ Stack Tecnológico y Dependencias
El entorno virtual de este proyecto ha sido configurado bajo **Python 3.11** utilizando un conjunto de librerías de grado de producción:

* **Core AI & Deep Learning:** * `tensorflow` (v2.21.0) & `keras` (v3.14.1): Infraestructura principal para la creación, entrenamiento y optimización de redes de aprendizaje profundo.
    * `ultralytics`: Framework utilizado para implementar arquitecturas **YOLO** (You Only Look Once) orientadas a la detección de objetos por computadora a alta velocidad.
* **Procesamiento de Datos y Análisis Predictivo:**
    * `numpy` & `polars`: Manipulación eficiente de matrices de alta dimensionalidad y dataframes a gran escala con alto rendimiento.
    * `scikit-learn`: Utilizado para la separación de conjuntos de datos (train/test), ingeniería de características (*feature engineering*) y validación mediante matrices de confusión y métricas de evaluación (F1-Score, Precision, Recall).
* **Procesamiento de Imágenes y Visualización:**
    * `opencv-python` (OpenCV): Librería clave para la manipulación, reescalado y filtrado de flujos de imágenes y vídeo.
    * `matplotlib`: Generación de gráficos analíticos de curvas de aprendizaje (Loss vs. Epochs) e históricos de precisión (Accuracy).

---

## 🚀 Estructura del Repositorio
```text
├── data/                  # Datasets utilizados (Imágenes, anotaciones YOLO y archivos estructurados)
├── notebooks/             # Notebooks de desarrollo y experimentación iterativa
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_tensorflow_deep_learning.ipynb
│   └── 03_yolo_object_detection.ipynb
├── models/                # Modelos entrenados guardados en formato (.h5, .keras, .pt)
├── src/                   # Scripts de Python refactorizados para producción (.py)
├── requirements.txt       # Archivo de dependencias del proyecto
└── README.md              # Documentación técnica (este archivo)
