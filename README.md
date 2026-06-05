# InsurTech & Computer Vision: Plataforma Inteligente de Auditoría de Siniestros y Control de Fraude Financiero

## 📊 Vista General del Proyecto
Este proyecto presenta una **Prueba de Concepto (PoC) de grado de producción** orientada al sector asegurador para la **automatización, auditoría analítica de costes y prevención de fraude en seguros de automóviles**. 

A través de la implementación de arquitecturas de aprendizaje profundo (Deep Learning) y computación visual, el sistema simula el flujo completo de una aseguradora moderna: recibe las imágenes de los siniestros tomadas en el taller, clasifica y valida los vehículos automáticamente mediante un modelo **YOLOv8**, implementa un módulo de gobernanza del dato para la captura de matrícula e importe económico por parte del perito, y consolida un histórico financiero interactivo en un Cuadro de Mando (*Dashboard*).

El sistema destaca por resolver un problema crítico de negocio: el **cotejo pericial** (*cross-checking*). El analista de la oficina puede auditar de forma visual e inmediata si un presupuesto de reparación solicitado está en consonancia con la gravedad de los impactos procesados por la Inteligencia Artificial.

---

## 🛠️ Arquitectura de Procesamiento y Flujo de Datos

El sistema implementa una arquitectura unificada dividida en dos grandes etapas operativas:

### ⚙️ Fase 1: Ingesta Masiva y Trazabilidad en Origen (Script de Captura)
El motor de procesamiento central procesa las carpetas de siniestros de manera independiente ejecutando un flujo defensivo y estructurado:
1. **Validación Visual de la IA (Camino A):** El modelo YOLOv8 analiza cada imagen. Si detecta el vehículo completo (`class: car`) con una confianza $\ge 60\%$, la imagen se indexa automáticamente como "Toma General de Validación".
2. **Desvío por Excepción (Camino B):** Si la imagen representa un plano cerrado de un impacto, una pieza suelta o no supera el umbral de confianza, el algoritmo la desvía al flujo de "Revisión Manual de Daños".
3. **Gobierno del Dato (Human-in-the-Loop):** El script congela la ejecución y exige al perito responsable introducir la matrícula del vehículo y el **Presupuesto Inicial de Reparación**. El sistema valida que el importe sea un formato numérico flotante real antes de firmar el expediente.
4. **Persistencia Estructurada:** Genera archivos `.json` independientes de auditoría que contienen la metadata del siniestro, las rutas de las fotos clasificadas, el coste económico y la firma digital del usuario responsable (`PERITO_CARLOS_GOMEZ`).

### 🖥️ Fase 2: Cuadro de Mando de Control Financiero (Portal Streamlit en Localhost)
La aplicación web simula el entorno Cloud corporativo de la aseguradora en un servidor local (`localhost`).
* **Consolidación en RAM:** Lee en tiempo real todos los JSON de la carpeta de salida y los transforma en un DataFrame de `pandas`.
* **Métricas de Impacto de Negocio (KPIs):** Muestra el volumen total de siniestros, el coste acumulado total de las reparaciones de la cartera, el inventario de fotos y el presupuesto medio.
* **Filtros Cruzados:** Permite al analista de oficina buscar expedientes instantáneamente mediante filtros por ID de Siniestro o mediante búsqueda predictiva por texto de la matrícula del vehículo.
* **Alertas Automatizadas de Fraude:** Si un expediente individual supera el umbral de riesgo de **1.000 €**, el portal genera dinámicamente un banner de advertencia (*Warning*) para alertar al analista de que cruce minuciosamente las fotos de los impactos con el dinero solicitado.

---

## 💼 Impacto de Negocio & Mitigación del Fraude (Business Case)
Este prototipo transforma la operativa tradicional de seguros en un ecosistema de alta eficiencia:
* **Mitigación del Ratios Combinados:** Evita el pago de reclamaciones infladas o presupuestos desproporcionados mediante alertas automatizadas basadas en el coste.
* **Gobernanza y Responsabilidad:** Al requerir firmas periciales y capturar datos estructurados desde el input, se garantiza la trazabilidad legal del expediente: se sabe exactamente quién cargó la información y qué monto se autorizó inicialmente.
* **Eficiencia Operativa:** Automatiza la validación de los casos estándar y permite que el equipo de analistas enfoque sus esfuerzos de investigación exclusivamente en los siniestros identificados como de alto riesgo.

---

## 🛠️ Stack Tecnológico y Dependencias
El entorno virtual de este proyecto (`venv`) ha sido desarrollado bajo **Python 3.11**, utilizando herramientas de alto rendimiento para el análisis de datos y la inteligencia artificial:

* **Core AI & Visión Artificial:**
    * `ultralytics` (YOLOv8): Red neuronal utilizada para la localización y verificación del vehículo a alta velocidad.
* **Estructuración y Analítica de Datos:**
    * `pandas`: Motor tabular utilizado para la carga, limpieza, filtrado y cálculo de agregaciones financieras de los expedientes.
    * `json` & `os`: Librerías nativas para el gobierno de archivos, persistencia en disco y manejo del sistema de archivos.
* **Interfaz de Usuario e Infraestructura Web:**
    * `streamlit`: Framework utilizado para desplegar la aplicación interactiva en servidor web local (`localhost:8501`) sin necesidad de complejas arquitecturas frontend.

---

## 🚀 Estructura del Repositorio Actualizada

```text
├── data/
│   ├── input_imagenes/       # Carpetas de siniestros (contienen los JPGs subidos por los peritos)
│   │   ├── SIN-2026-001/
│   │   └── SIN-2026-002/
│   └── out_put_json/         # Base de conocimientos estructurada (JSONs generados firmados con metadatos)
├── modelos/                  # Almacenamiento local del peso de la red neuronal (yolov8n.pt)
├── notebooks/                # Cuadernos Jupyter para el desarrollo experimental y pruebas iniciales
├── app_analista.py           # Aplicación principal del Dashboard Financiero e interactivo (Streamlit)
├── .gitignore                # Reglas de exclusión de Git (excluye entornos virtuales y datos pesados)
└── requirements.txt          # Congelación de dependencias del entorno virtual (generado vía pip freeze)