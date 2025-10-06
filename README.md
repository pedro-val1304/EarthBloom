# README.md — EarthBloom (ES/EN)

![EarthBloom Logo](images/logo_1.png)  
![NASA Space Apps Challenge](images/nasa.png)

---

## Español

### Descripción
**EarthBloom** es una plataforma científica desarrollada para el **NASA Space Apps Challenge 2025**. Apoya a investigadores que estudian la fenología vegetal y sus respuestas al cambio climático. Integra **datos satelitales**, **meteorológicos** y **observaciones de campo verificadas** con **modelos espacio-temporales de aprendizaje automático** para generar mapas dinámicos que estiman zonas y periodos potenciales de floración.

Beneficios clave:
- Optimiza campañas de campo enfocando recursos en **áreas de mayor interés ecológico**.
- **Reduce costos** de muestreo innecesarios.
- **Aumenta la precisión** de análisis de impacto climático.

Estado del proyecto:
- Este repositorio contiene una **DEMO** basada en front-end estático.
- Algunas funciones (por ejemplo, **registro para agregar puntos de interés**) aún **no están operativas** y se muestran como vistas o placeholders.
- El objetivo es **no comercial** y **científico**; buscamos infraestructura confiable para análisis fenológicos predictivos.

Documentación incluida:
- Documento: **EarthBloom_English.docx** con la memoria/justificación científica (introducción, problema, solución, tecnologías, impacto, escalabilidad, equipo y referencias APA).

Trabajos futuros:
- Integrar **más bases de datos** (HLS, MODIS, VIIRS, estaciones meteorológicas, GBIF/iNaturalist verificado, etc.).
- **Distinguir especies** con mejores modelos y criterios de **fenofases** para investigación más específica.
- Habilitar el **registro de observaciones verificadas** (carga de evidencias, revisión ligera por pares, control de calidad).
- **Descargas reproducibles** (GeoTIFF/CSV) con metadatos estándar (p. ej., Darwin Core), **DOIs** y **versionado**.

### Cómo visualizar la DEMO localmente
Requisitos:
- **Visual Studio Code**
- Extensión **Live Server** (Ritwick Dey o equivalente)
- **Navegador moderno**

Pasos (Fork recomendado):
1. Haz **Fork** del repositorio en tu cuenta de GitHub.  
2. Clona tu fork:
   - HTTPS:
     ```bash
     git clone https://github.com/TU_USUARIO/EarthBloom.git
     ```
   - SSH:
     ```bash
     git clone git@github.com:TU_USUARIO/EarthBloom.git
     ```
3. Abre la carpeta del repositorio con **Visual Studio Code**.  
4. Instala/activa la extensión **Live Server**.  
5. En el explorador de VS Code, clic derecho sobre `index.html` → **Open with Live Server**.

Páginas clave:
- `index.html` → Página principal.  
- `mapa.html` → **DEMO** del mapa/visualización.

Si no ves estilos/imágenes:
- Revisa la estructura de carpetas (`css/`, `images/`) y rutas relativas.  
- Haz una **recarga dura** del navegador (Ctrl/Cmd+Shift+R).

### Estructura sugerida
```
.
├─ index.html
├─ mapa.html
├─ flores.html
├─ nuestro_equipo.html
├─ css/
│  └─ main.css
├─ images/
│  ├─ logo_1.png
│  └─ nasa.png
├─ script.js        (si aplica)
└─ EarthBloom_English.docx
```

### Tecnologías (Front DEMO)
- **HTML, CSS, JavaScript**
- **Leaflet**, **OpenStreetMap** (mapa DEMO)
- **GeoJSON** (mock/placeholder)

### Autores / Equipo (de `nuestro_equipo.html`)
- **Héctor Tadeo Cadena Alfaro** — Backend  
- **Emiliano Becerra López** — Líder  
- **Ángel Gael Álvarez López** — Data Analyst  
- **José Pedro Valenzuela López** — Frontend  
- **Pedro Daniel Gutiérrez Pérez** — Frontend  
- **Daniel Alberto Curiel Vargas** — Documentación

### Licencia
Proyecto **no comercial**, orientado a **investigación** y **ciencia abierta**. Sugerido: MIT/Apache-2.0/CC-BY (definir según necesidad).

### Atribuciones
- NASA Space Apps Challenge (`images/nasa.png`).  
- EarthBloom (`images/logo_1.png`).  
- Bibliotecas/datos citados en el repositorio o en la documentación.

**Contacto**  
- Email: jose.valenzuela6861@alumnos.udg.mx  
- GitHub: https://github.com/pedro-val1304/EarthBloom

---

## English

### Overview
**EarthBloom** is a scientific platform developed for the **NASA Space Apps Challenge 2025** to support researchers studying plant phenology under climate change. It integrates **satellite**, **meteorological**, and **verified field observations** using **spatiotemporal machine learning** to produce dynamic maps estimating potential bloom areas and timing.

Key benefits:
- Optimizes field campaigns by focusing resources on **high-interest ecological areas**.  
- **Reduces costs** from unnecessary sampling.  
- **Improves precision** of climate impact analyses.

Project status:
- This repository ships a **DEMO** using a static front-end.  
- Some features (e.g., the **submission/registration to add points of interest**) are **not yet operational** and appear as placeholders.  
- The project is **non-commercial** and **research-oriented**, aiming to provide reliable infrastructure for predictive phenology.

Included documentation:
- File: **EarthBloom_English.docx** with the scientific write-up (introduction, problem, solution, technologies, impact, scalability, team, APA references).

Future work:
- Integrate **additional datasets** (HLS, MODIS, VIIRS, weather stations, GBIF/verified iNaturalist, etc.).  
- **Improve species discrimination** via models and **phenophase** criteria for more specific research.  
- Enable **verified observation submission** (evidence upload, light peer review, quality control).  
- Provide **reproducible downloads** (GeoTIFF/CSV) with standard metadata (e.g., Darwin Core), **DOIs**, and **versioning**.

### How to run the DEMO locally
Requirements:
- **Visual Studio Code**
- **Live Server** extension (by Ritwick Dey or equivalent)
- **Modern browser**

Steps (Fork recommended):
1. **Fork** this repository to your GitHub account.  
2. Clone your fork:
   - HTTPS:
     ```bash
     git clone https://github.com/YOUR_USER/EarthBloom.git
     ```
   - SSH:
     ```bash
     git clone git@github.com:YOUR_USER/EarthBloom.git
     ```
3. Open the repository folder in **Visual Studio Code**.  
4. Install/enable **Live Server** extension.  
5. In VS Code, right‑click `index.html` → **Open with Live Server**.

Key pages:
- `index.html` → Main landing page.  
- `mapa.html` → Map/visualization **DEMO**.

If styles/images don’t load:
- Verify folder structure (`css/`, `images/`) and relative paths.  
- Perform a **hard refresh** (Ctrl/Cmd+Shift+R).

### Suggested structure
```
.
├─ index.html
├─ mapa.html
├─ flores.html
├─ nuestro_equipo.html
├─ css/
│  └─ main.css
├─ images/
│  ├─ logo_1.png
│  └─ nasa.png
├─ script.js        (if applicable)
└─ EarthBloom_English.docx
```

### Technologies (Front DEMO)
- **HTML, CSS, JavaScript**
- **Leaflet**, **OpenStreetMap** (map DEMO)
- **GeoJSON** (mock/placeholder)

### Authors / Team (from `nuestro_equipo.html`)
- **Héctor Tadeo Cadena Alfaro** — Backend  
- **Emiliano Becerra López** — Leader  
- **Ángel Gael Álvarez López** — Data Analyst  
- **José Pedro Valenzuela López** — Frontend  
- **Pedro Daniel Gutiérrez Pérez** — Frontend  
- **Daniel Alberto Curiel Vargas** — Documentation

### License
**Non-commercial**, **research-oriented** project. Suggested: MIT/Apache‑2.0/CC‑BY (choose as needed).

### Acknowledgements
- NASA Space Apps Challenge (`images/nasa.png`).  
- EarthBloom (`images/logo_1.png`).  
- Libraries/datasets referenced in the repo or in the documentation.

**Contact**  
- Email: jose.valenzuela6861@alumnos.udg.mx  
- GitHub: https://github.com/pedro-val1304/EarthBloom
