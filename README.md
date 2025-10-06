### EarthBloom (ES/EN)

<p align="center">
  <img href="https://cdn.abacus.ai/images/1a828090-01be-428a-a51a-f6ee84559d4c.png" alt="EarthBloom" width="100%">
</p>

<p align="center">
  <a href="https://github.com/pedro-val1304/EarthBloom"><img src="https://img.shields.io/badge/status-DEMO-blue?style=for-the-badge" alt="Status"></a>
  <a href="https://github.com/pedro-val1304/EarthBloom/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/pedro-val1304/EarthBloom/issues"><img src="https://img.shields.io/github/issues/pedro-val1304/EarthBloom?style=for-the-badge&color=orange" alt="Issues"></a>
  <a href="https://github.com/pedro-val1304/EarthBloom/stargazers"><img src="https://img.shields.io/github/stars/pedro-val1304/EarthBloom?style=for-the-badge&color=yellow" alt="Stars"></a>
  <a href="https://spaceappschallenge.org/"><img src="https://img.shields.io/badge/NASA%20Space%20Apps-2025-0b3d91?style=for-the-badge" alt="NASA Space Apps 2025"></a>
</p>

<p align="center">
  <img src="images/logo_1.png" alt="EarthBloom Logo" height="64">
  &nbsp;&nbsp;
  <img src="images/nasa.png" alt="NASA Space Apps Challenge" height="64">
</p>

---

## Tabla de contenidos
- [Español](#español)
  - [Descripción](#-earthbloom)
  - [DEMO](#demo)
  - [Quick Start](#-quick-start)
  - [Ejecutar la DEMO localmente](#-ejecutar-la-demo-localmente)
  - [Arquitectura (DEMO)](#-arquitectura-demo)
  - [Tecnologías](#tecnologías)
  - [Equipo](#-equipo)
  - [Cómo contribuir](#-cómo-contribuir)
  - [Código de conducta](#-código-de-conducta)
  - [Licencia](#-licencia)
  - [Contacto](#contacto)
- [English](#english)
  - [Overview](#-overview)
  - [DEMO](#demo-1)
  - [Quick Start](#-quick-start-1)
  - [Run locally](#-run-the-demo-locally)
  - [Structure (DEMO)](#-structure-demo)
  - [Technologies](#technologies-front-demo)
  - [Team](#-team)
  - [Contributing](#-contributing)
  - [Code of Conduct](#-code-of-conduct)
  - [License](#-license)
  - [Contact](#contact-1)

---

## Español

### 🌱 EarthBloom
EarthBloom es una plataforma científica desarrollada para el NASA Space Apps Challenge 2025. Apoya a investigadores que estudian la fenología vegetal y sus respuestas al cambio climático. Integra datos satelitales, meteorológicos y observaciones de campo verificadas con modelos espacio‑temporales de aprendizaje automático para generar mapas dinámicos que estiman zonas y periodos potenciales de floración.

- Enfoque: ciencia abierta, no comercial.
- Público objetivo: investigadores y organizaciones ambientales.

#### Beneficios clave
- Priorización de campañas de campo en áreas de mayor valor ecológico.
- Reducción de costos de muestreo redundante.
- Mayor precisión en el análisis de impacto climático y fenofases.

#### Estado del proyecto
- Este repositorio contiene una DEMO basada usando los datos otorgados, siendo un MVP.
- Algunas funciones (p. ej., registro para agregar puntos de interés) aún no están operativas y se muestran como vistas/placeholder.
- Documentación incluida: EarthBloom_English.docx 

#### Roadmap
- Integrar más bases de datos (HLS, MODIS, VIIRS, estaciones meteorológicas, GBIF/iNaturalist verificado, etc.).
- Mejor discriminación por especie y criterios de fenofases.
- Registro de observaciones verificadas (evidencias, revisión ligera por pares, control de calidad).
- Descargas reproducibles (GeoTIFF/CSV) con metadatos estándar (Darwin Core), DOIs y versionado.

### 🚀 Ejecutar la DEMO localmente
Requisitos
- Visual Studio Code
- Extensión Live Server (Ritwick Dey o equivalente)
- Navegador moderno

Pasos (Fork recomendado)
1. Haz Fork del repositorio y clónalo:
   - HTTPS:
     ```bash
     git clone https://github.com/TU_USUARIO/EarthBloom.git
     ```
   - SSH:
     ```bash
     git clone git@github.com:TU_USUARIO/EarthBloom.git
     ```
2. Abre la carpeta en VS Code.  
3. Instala/activa Live Server.  
4. Clic derecho en `index.html` → Open with Live Server.

Páginas clave
- `index.html` → Landing page.  
- `mapa.html` → DEMO del mapa/visualización.

Solución de problemas
- Si no cargan estilos/imágenes: verifica rutas relativas y estructura (`css/`, `images/`) y realiza una recarga dura (Ctrl/Cmd+Shift+R).

### Tecnologías
- HTML, CSS, JavaScript
- Leaflet + OpenStreetMap (mapa DEMO)
- GeoJSON (mock/placeholder)

### 👥 Equipo
- Héctor Tadeo Cadena Alfaro — Backend  
- Emiliano Becerra López — Backend  
- Ángel Gael Álvarez López — Data Analyst  
- José Pedro Valenzuela López — Frontend  
- Pedro Daniel Gutiérrez Pérez — Frontend  
- Daniel Alberto Curiel Vargas — Documentación

### 🤝 Cómo contribuir
¡Contribuciones bienvenidas! Sugerimos:
1. Revisa los Issues o crea uno nuevo con la etiqueta `enhancement` o `bug`.
2. Haz Fork y crea una rama descriptiva:
   ```bash
   git checkout -b feature/mejora-x
   ```
3. Realiza cambios y añade capturas/pruebas si aplica.  
4. Pasa linter/formatter (HTML/CSS/JS).  
5. Abre un Pull Request explicando objetivo, cambios y evidencia visual.

Pautas:
- Mantén un tono científico y datos trazables.
- Para nuevos datasets, incluye fuentes, licencias y metadatos.
- No subas datos sensibles ni materiales con derechos restrictivos.

### 🔐 Licencia
Proyecto no comercial, orientado a investigación y ciencia abierta. Publicado bajo [MIT](LICENSE) salvo indicación distinta.

### Contacto
- Email: jose.valenzuela6861@alumnos.udg.mx | emiliano.becerra5451@alumnos.udg.mx  
- GitHub: https://github.com/pedro-val1304/EarthBloom

---

## English

### 🌸 Overview
EarthBloom is a scientific platform for the NASA Space Apps Challenge 2025 to support researchers studying plant phenology under climate change. It integrates satellite and meteorological data with verified field observations and spatiotemporal ML to generate dynamic maps estimating potential bloom areas and timing.

- Focus: open science, non‑commercial.  
- Audience: researchers and NGOs.

#### Key benefits
- Prioritize field campaigns in high‑value ecological regions.  
- Reduce redundant sampling costs.  
- Improve climate‑impact and phenophase analyses.

#### Project status
- Basic DEMO as an MVP.  
- Some features are placeholders (POI submission, observation upload).  
- Included doc: EarthBloom_English.docx
- 
#### Roadmap
- Add datasets (HLS, MODIS, VIIRS, weather stations, GBIF/verified iNaturalist).  
- Better species discrimination and phenophase criteria.  
- Verified observation submission (evidence, light peer review, QC).  
- Reproducible downloads (GeoTIFF/CSV) with standard metadata, DOIs, versioning.

### 🚀 Run the DEMO locally
Requirements
- Visual Studio Code  
- Live Server extension  
- Modern browser

Steps (Fork recommended)
1. Fork and clone:
   - HTTPS:
     ```bash
     git clone https://github.com/YOUR_USER/EarthBloom.git
     ```
   - SSH:
     ```bash
     git clone git@github.com:YOUR_USER/EarthBloom.git
     ```
2. Open the folder in VS Code.  
3. Install/enable Live Server.  
4. Right‑click `index.html` → Open with Live Server.

Key pages
- `index.html` → Landing page.  
- `mapa.html` → Map/visualization DEMO.

Troubleshooting
- If styles/images don’t load: verify relative paths and structure (`css/`, `images/`), then hard refresh (Ctrl/Cmd+Shift+R).

### Technologies (Front DEMO)
- HTML, CSS, JavaScript  
- Leaflet + OpenStreetMap  
- GeoJSON (mock/placeholder)

### 👤 Team
- Héctor Tadeo Cadena Alfaro — Backend  
- Emiliano Becerra López — Backend  
- Ángel Gael Álvarez López — Data Analyst  
- José Pedro Valenzuela López — Frontend  
- Pedro Daniel Gutiérrez Pérez — Frontend  
- Daniel Alberto Curiel Vargas — Documentation


### 📄 License
Non‑commercial, research‑oriented. Released under [MIT](LICENSE) unless otherwise stated.

### Contact
- Email: emiliano.becerra5451@alumnos.udg.mx | jose.valenzuela6861@alumnos.udg.mx  
- GitHub: https://github.com/pedro-val1304/EarthBloom

---
