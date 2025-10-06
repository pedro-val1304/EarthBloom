import os
from flask import Flask, render_template, request, jsonify, send_file
import json
import numpy as np
from datetime import datetime
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import haversine_distances
import tempfile
import shutil
from math import radians

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class WildflowerMLSystem:
    def __init__(self):
        # Usar rutas absolutas basadas en la ubicación del script
        self.primary_geojson = os.path.join(BASE_DIR, 'WildflowerBlooms_AreaOfInterest.geojson')
        self.combined_geojson = os.path.join(BASE_DIR, 'WildflowerBlooms_Combined.geojson')
        self.user_points_file = os.path.join(BASE_DIR, 'user_points.json')
        self.ml_vertices_file = os.path.join(BASE_DIR, 'ml_vertices.json')
        
        # Inicializar la base de datos combinada
        self.initialize_combined_database()
        self.load_data()
        
        # Generar polígonos ML automáticamente al iniciar
        self.auto_generate_ml_polygons()
    
    def initialize_combined_database(self):
        """Inicializa la base de datos combinada con los datos originales si no existe"""
        if not os.path.exists(self.combined_geojson):
            try:
                # Verificar que el archivo original existe
                if os.path.exists(self.primary_geojson):
                    # Copiar los datos originales a la base de datos combinada
                    shutil.copyfile(self.primary_geojson, self.combined_geojson)
                    print("✅ Base de datos combinada creada a partir de datos originales")
                else:
                    print(f"❌ Archivo original no encontrado: {self.primary_geojson}")
                    # Crear una base de datos combinada vacía
                    with open(self.combined_geojson, 'w', encoding='utf-8') as f:
                        json.dump({"type": "FeatureCollection", "features": []}, f, indent=2)
            except Exception as e:
                print(f"❌ Error inicializando base de datos combinada: {e}")
                # Crear una base de datos combinada vacía
                with open(self.combined_geojson, 'w', encoding='utf-8') as f:
                    json.dump({"type": "FeatureCollection", "features": []}, f, indent=2)
                    
    def load_data(self):
        # Cargar ÚNICAMENTE la base de datos combinada
        try:
            with open(self.combined_geojson, 'r', encoding='utf-8') as f:
                self.combined_data = json.load(f)
            print(f"✅ Base de datos combinada cargada: {len(self.combined_data.get('features', []))} features")
        except Exception as e:
            print(f"❌ Error cargando base de datos combinada: {e}")
            self.combined_data = {"type": "FeatureCollection", "features": []}
        
        # Cargar puntos de usuario
        try:
            with open(self.user_points_file, 'r', encoding='utf-8') as f:
                self.user_points = json.load(f)
            print(f"✅ Puntos de usuario cargados: {len(self.user_points)} puntos")
        except:
            self.user_points = []
            print("✅ Puntos de usuario inicializados (archivo no existía)")
        
        # Cargar vértices ML
        try:
            with open(self.ml_vertices_file, 'r', encoding='utf-8') as f:
                self.ml_vertices = json.load(f)
            print(f"✅ Vértices ML cargados: {len(self.ml_vertices)} vértices")
        except:
            self.ml_vertices = []
            print("✅ Vértices ML inicializados (archivo no existía)")
    
    def save_combined_data(self):
        """Guarda la base de datos combinada"""
        try:
            with open(self.combined_geojson, 'w', encoding='utf-8') as f:
                json.dump(self.combined_data, f, indent=2)
            print(f"✅ Base de datos combinada guardada: {len(self.combined_data.get('features', []))} features")
            return True
        except Exception as e:
            print(f"❌ Error guardando base de datos combinada: {e}")
            return False
    
    def save_user_points(self):
        try:
            with open(self.user_points_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_points, f, indent=2)
            print(f"✅ Puntos de usuario guardados: {len(self.user_points)} puntos")
            return True
        except Exception as e:
            print(f"❌ Error guardando puntos de usuario: {e}")
            return False
    
    def save_ml_vertices(self):
        try:
            with open(self.ml_vertices_file, 'w', encoding='utf-8') as f:
                json.dump(self.ml_vertices, f, indent=2)
            print(f"✅ Vértices ML guardados: {len(self.ml_vertices)} vértices")
            return True
        except Exception as e:
            print(f"❌ Error guardando vértices ML: {e}")
            return False
    
    def extract_points_from_combined_data(self):
        """Extrae TODOS los puntos de la base de datos combinada"""
        all_points = []
        
        for feature in self.combined_data.get("features", []):
            geometry = feature.get("geometry", {})
            properties = feature.get("properties", {})
            
            if geometry.get("type") == "Polygon":
                for ring in geometry.get("coordinates", []):
                    for coord in ring:
                        if len(coord) >= 2:
                            all_points.append({
                                "lng": coord[0],
                                "lat": coord[1],
                                "source": "combined_polygon",
                                "properties": properties
                            })
            elif geometry.get("type") == "MultiPolygon":
                for polygon in geometry.get("coordinates", []):
                    for ring in polygon:
                        for coord in ring:
                            if len(coord) >= 2:
                                all_points.append({
                                    "lng": coord[0],
                                    "lat": coord[1],
                                    "source": "combined_multipolygon", 
                                    "properties": properties
                                })
        
        # Añadir puntos de usuario
        for point in self.user_points:
            all_points.append({
                "lng": point.get("lng"),
                "lat": point.get("lat"),
                "source": "user",
                "properties": point
            })
        
        print(f"📊 Puntos extraídos para ML: {len(all_points)} puntos totales")
        return all_points
    
    def cluster_points(self, points, eps=0.05, min_samples=3):
        """
        Agrupa puntos usando DBSCAN - ALGORITMO DE MACHINE LEARNING
        
        DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
        es un algoritmo de clustering basado en densidad que:
        
        1. Identifica puntos centrales en regiones densas
        2. Agrupa puntos que están suficientemente cerca (dentro de ε)
        3. Considera puntos aislados como ruido
        
        Parámetros:
        - eps (ε): Radio de búsqueda para encontrar vecinos (0.05 grados ≈ 5.5 km)
        - min_samples: Mínimo de puntos para formar un cluster denso (3 puntos)
        """
        if len(points) < 3:
            return []
        
        coords = [[p['lng'], p['lat']] for p in points]
        
        # Usar DBSCAN para clustering - MACHINE LEARNING
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(coords)
        
        # Análisis de los resultados del clustering
        unique_labels = set(labels)
        n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
        n_noise = list(labels).count(-1)
        
        print(f"🔍 DBSCAN encontró {n_clusters} clusters y {n_noise} puntos de ruido")
        
        clusters = {}
        for i, label in enumerate(labels):
            if label != -1:  # Ignorar ruido (-1)
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(points[i])
        
        print(f"🔍 Clusters válidos para polígonos: {len(clusters)} clusters")
        return list(clusters.values())
    
    def convex_hull(self, points):
        """
        Algoritmo del Gift Wrapping (Jarvis March) para calcular la envolvente convexa
        
        Este algoritmo:
        1. Encuentra el punto más a la izquierda como punto inicial
        2. Para cada punto, encuentra el punto que forma el menor giro a la izquierda
        3. Continúa hasta volver al punto inicial
        
        La envolvente convexa representa el área mínima que contiene todos los puntos
        """
        if len(points) < 3:
            return None
        
        # Convertir a array de coordenadas
        coords = [[p['lng'], p['lat']] for p in points]
        
        # Encontrar el punto más a la izquierda
        leftmost = min(coords, key=lambda p: p[0])
        
        hull = []
        current_point = leftmost
        
        while True:
            hull.append(current_point)
            next_point = coords[0]
            
            for point in coords:
                if (next_point == current_point or 
                    self.cross_product(current_point, next_point, point) > 0):
                    next_point = point
            
            current_point = next_point
            
            if current_point == leftmost:
                break
        
        # Cerrar el polígono
        if hull and hull[0] != hull[-1]:
            hull.append(hull[0])
            
        return hull
    
    def cross_product(self, o, a, b):
        """Producto cruzado para determinar orientación (sentido horario/antihorario)"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def calculate_area(self, polygon):
        """Calcula área usando fórmula del shoelace (Gauss)"""
        if len(polygon) < 3:
            return 0.0
        
        area = 0.0
        n = len(polygon)
        
        for i in range(n):
            j = (i + 1) % n
            area += polygon[i][0] * polygon[j][1]
            area -= polygon[j][0] * polygon[i][1]
        
        return abs(area) / 2.0 * 111000 * 111000  # Convertir a m²
    
    def calculate_polygon_centroid(self, polygon_coords):
        """
        Calcula el centroide (centro geométrico) de un polígono
        
        El centroide es el punto promedio de todos los vértices del polígono
        y se usa para el heatmap en lugar de los vértices individuales
        """
        if len(polygon_coords) < 3:
            return None
            
        lons = [coord[0] for coord in polygon_coords]
        lats = [coord[1] for coord in polygon_coords]
        
        centroid_lon = sum(lons) / len(lons)
        centroid_lat = sum(lats) / len(lats)
        
        return [centroid_lon, centroid_lat]
    
    def extract_ml_vertices(self, ml_polygons):
        """
        Extrae todos los vértices de los polígonos ML como puntos individuales
        
        Cada vértice se guarda como un punto visible en el mapa, similar a los
        puntos de investigación del usuario
        """
        vertices = []
        
        for polygon in ml_polygons:
            properties = polygon.get("properties", {})
            coordinates = polygon.get("geometry", {}).get("coordinates", [])
            
            if coordinates:
                for ring in coordinates:
                    for coord in ring:
                        vertex = {
                            "id": f"ml_vertex_{len(vertices)}_{datetime.now().strftime('%H%M%S')}",
                            "lng": coord[0],
                            "lat": coord[1],
                            "source_polygon": properties.get("Site", "ML Polygon"),
                            "type": "ML Vertex",
                            "season": "Auto-generated",
                            "area": 0,
                            "timestamp": datetime.now().isoformat()
                        }
                        vertices.append(vertex)
        
        return vertices
    
    def auto_generate_ml_polygons(self):
        """Genera polígonos ML automáticamente al iniciar el sistema"""
        print("🔄 Generando polígonos ML automáticamente...")
        
        # Extraer TODOS los puntos de la base de datos combinada + puntos usuario
        all_points = self.extract_points_from_combined_data()
        
        if len(all_points) < 3:
            print("❌ No hay suficientes puntos para generar polígonos ML automáticamente")
            return
        
        # Agrupar puntos usando DBSCAN
        clusters = self.cluster_points(all_points, eps=0.05, min_samples=3)
        
        new_polygons = []
        
        for i, cluster in enumerate(clusters):
            if len(cluster) >= 3:
                try:
                    hull = self.convex_hull(cluster)
                    if hull and len(hull) >= 4:
                        area = self.calculate_area(hull)
                        
                        # Encontrar fuentes únicas
                        sources = set()
                        user_count = 0
                        original_polygons = set()
                        
                        for point in cluster:
                            if point.get("source") == "user":
                                user_count += 1
                            sources.add(point.get("source", "unknown"))
                            
                            # Identificar polígonos originales involucrados
                            props = point.get("properties", {})
                            if props.get("Site"):
                                original_polygons.add(props.get("Site"))
                        
                        polygon_feature = {
                            "type": "Feature",
                            "properties": {
                                "id": f"ml_auto_{i}_{datetime.now().strftime('%H%M%S')}",
                                "Site": f"Área ML Auto {i+1}",
                                "Type": "ML Generated",
                                "Season": "Variable", 
                                "Area": area,
                                "point_count": len(cluster),
                                "user_points": user_count,
                                "sources": list(sources),
                                "original_polygons_involved": list(original_polygons),
                                "generated_auto": True,
                                "auto_generated": True,
                                "timestamp": datetime.now().isoformat()
                            },
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [hull]
                            }
                        }
                        
                        new_polygons.append(polygon_feature)
                        print(f"✅ Polígono ML Auto {i+1} generado con {len(cluster)} puntos")
                        
                except Exception as e:
                    print(f"❌ Error creando polígono ML automático: {e}")
        
        if new_polygons:
            # Agregar nuevos polígonos a la base de datos combinada
            existing_features = self.combined_data.get("features", [])
            
            # Eliminar polígonos ML auto-generados anteriores para evitar duplicados
            existing_features = [f for f in existing_features 
                               if not f.get("properties", {}).get("auto_generated", False)]
            
            # Añadir los nuevos polígonos auto-generados
            existing_features.extend(new_polygons)
            self.combined_data["features"] = existing_features
            
            # Extraer y guardar vértices de los polígonos ML
            self.ml_vertices = self.extract_ml_vertices(new_polygons)
            self.save_ml_vertices()
            
            self.save_combined_data()
            print(f"✅ {len(new_polygons)} polígonos ML generados automáticamente")
            print(f"✅ {len(self.ml_vertices)} vértices ML extraídos")
        else:
            print("ℹ️ No se generaron nuevos polígonos ML automáticamente")
    
    def generate_ml_polygons(self):
        """Genera polígonos usando machine learning desde la base de datos combinada"""
        # Extraer TODOS los puntos de la base de datos combinada + puntos usuario
        all_points = self.extract_points_from_combined_data()
        
        if len(all_points) < 3:
            return {
                "status": "insufficient_points",
                "message": "No hay suficientes puntos para generar polígonos",
                "polygons": self.combined_data
            }
        
        # Agrupar puntos usando DBSCAN
        clusters = self.cluster_points(all_points, eps=0.05, min_samples=3)
        
        new_polygons = []
        
        for i, cluster in enumerate(clusters):
            if len(cluster) >= 3:
                try:
                    hull = self.convex_hull(cluster)
                    if hull and len(hull) >= 4:
                        area = self.calculate_area(hull)
                        
                        # Encontrar fuentes únicas
                        sources = set()
                        user_count = 0
                        original_polygons = set()
                        
                        for point in cluster:
                            if point.get("source") == "user":
                                user_count += 1
                            sources.add(point.get("source", "unknown"))
                            
                            # Identificar polígonos originales involucrados
                            props = point.get("properties", {})
                            if props.get("Site"):
                                original_polygons.add(props.get("Site"))
                        
                        polygon_feature = {
                            "type": "Feature",
                            "properties": {
                                "id": f"ml_manual_{i}_{datetime.now().strftime('%H%M%S')}",
                                "Site": f"Área ML Manual {i+1}",
                                "Type": "ML Generated",
                                "Season": "Variable", 
                                "Area": area,
                                "point_count": len(cluster),
                                "user_points": user_count,
                                "sources": list(sources),
                                "original_polygons_involved": list(original_polygons),
                                "generated_auto": True,
                                "auto_generated": False,
                                "timestamp": datetime.now().isoformat()
                            },
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [hull]
                            }
                        }
                        
                        new_polygons.append(polygon_feature)
                        print(f"✅ Polígono ML Manual {i+1} generado con {len(cluster)} puntos")
                        
                except Exception as e:
                    print(f"❌ Error creando polígono ML manual: {e}")
        
        # Agregar nuevos polígonos a la base de datos combinada
        existing_features = self.combined_data.get("features", [])
        
        # Filtrar para evitar duplicados (basado en ID)
        new_polygon_ids = {p["properties"]["id"] for p in new_polygons}
        existing_features = [f for f in existing_features if f.get("properties", {}).get("id") not in new_polygon_ids]
        
        # Añadir los nuevos polígonos
        existing_features.extend(new_polygons)
        self.combined_data["features"] = existing_features
        
        # Extraer y guardar vértices de los polígonos ML
        if new_polygons:
            self.ml_vertices = self.extract_ml_vertices(new_polygons)
            self.save_ml_vertices()
        
        self.save_combined_data()
        
        return {
            "status": "success",
            "message": f"Generados {len(new_polygons)} polígonos con ML desde base de datos combinada",
            "polygons": self.combined_data
        }
    
    def add_user_point(self, point_data):
        """Añade punto de usuario"""
        point_id = f"user_point_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_point = {
            "id": point_id,
            "name": point_data.get("name", "Punto de usuario"),
            "type": point_data.get("type", "Wild"),
            "season": point_data.get("season", "Variable"),
            "area": point_data.get("area", 1000),
            "lat": point_data.get("lat"),
            "lng": point_data.get("lng"),
            "timestamp": datetime.now().isoformat()
        }
        
        self.user_points.append(new_point)
        self.save_user_points()
        
        print(f"✅ Punto de usuario añadido: {new_point['name']}")
        
        # Generar polígonos ML automáticamente después de añadir un punto
        self.auto_generate_ml_polygons()
        
        return new_point
    
    # app.py (modificar solo la función get_heatmap_data)
    def get_heatmap_data(self):
        """
        Genera datos para heatmap SOLO desde los CENTROIDES de polígonos ML
        Los puntos de usuario NO aparecen en el heatmap (son puntos visibles)
        """
        heatmap_data = []
        
        # Añadir SOLO centroides de polígonos ML (NO puntos de usuario)
        for feature in self.combined_data.get("features", []):
            properties = feature.get("properties", {})
            if properties.get("generated_auto", False):
                geometry = feature.get("geometry", {})
                if geometry.get("type") == "Polygon":
                    coords = geometry.get("coordinates", [])
                    if coords and len(coords) > 0:
                        centroid = self.calculate_polygon_centroid(coords[0])
                        if centroid:
                            heatmap_data.append({
                                "lng": centroid[0],
                                "lat": centroid[1],
                                "intensity": 1.0,
                                "source": "ml_centroid",
                                "polygon_name": properties.get("Site", "ML Polygon")
                            })
        
        print(f"🔥 Heatmap generado con {len(heatmap_data)} centroides ML (sin puntos usuario)")
        return {
            "point_count": len(heatmap_data),
            "heatmap_data": heatmap_data
        }
    
    def get_original_polygons(self):
        """Obtiene solo los polígonos originales (no generados por ML)"""
        original_features = []
        for feature in self.combined_data.get("features", []):
            properties = feature.get("properties", {})
            if not properties.get("generated_auto", False):
                original_features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": original_features
        }
    
    def get_ml_polygons(self):
        """Obtiene solo los polígonos generados por ML"""
        ml_features = []
        for feature in self.combined_data.get("features", []):
            properties = feature.get("properties", {})
            if properties.get("generated_auto", False):
                ml_features.append(feature)
        
        return {
            "type": "FeatureCollection", 
            "features": ml_features
        }
    
    def get_ml_explanation(self):
        """Proporciona una explicación detallada del Machine Learning utilizado"""
        explanation = {
            "algorithm": "DBSCAN (Density-Based Spatial Clustering of Applications with Noise)",
            "purpose": "Agrupar puntos geográficos basándose en su densidad espacial",
            "parameters": {
                "eps": 0.05,
                "min_samples": 3,
                "eps_meaning": "Radio de búsqueda (0.05 grados ≈ 5.5 km en el ecuador)",
                "min_samples_meaning": "Mínimo de puntos para formar un cluster denso"
            },
            "decision_criteria": {
                "core_points": "Puntos que tienen al menos min_samples vecinos dentro del radio eps",
                "border_points": "Puntos dentro del radio eps de un core point pero sin suficientes vecinos",
                "noise_points": "Puntos que no son core points ni border points (se descartan)",
                "cluster_formation": "Grupos conectados de core points y sus border points"
            },
            "polygon_formation": {
                "algorithm": "Gift Wrapping (Jarvis March) - Envolvente Convexa",
                "purpose": "Encontrar el polígono más pequeño que contiene todos los puntos del cluster",
                "output": "Polígono que representa el área de densidad detectada"
            },
            "advantages": [
                "No requiere especificar el número de clusters de antemano",
                "Puede encontrar clusters de forma arbitraria",
                "Robusto ante valores atípicos (ruido)",
                "Funciona bien con datos geográficos"
            ],
            "limitations": [
                "Sensible a los parámetros eps y min_samples",
                "Dificultad con clusters de densidad variable",
                "Rendimiento con grandes volúmenes de datos"
            ]
        }
        return explanation

# In

#Inicializar sistema ML
print("🚀 Inicializando Sistema ML de Wildflowers...")
ml_system = WildflowerMLSystem()

@app.route('/')
def index():
    return render_template('plugin.html')

@app.route('/api/combined-data')
def get_combined_data():
    return jsonify(ml_system.combined_data)

@app.route('/api/original-polygons')
def get_original_polygons():
    return jsonify(ml_system.get_original_polygons())

@app.route('/api/ml-polygons')
def get_ml_polygons():
    return jsonify(ml_system.get_ml_polygons())

@app.route('/api/user-points')
def get_user_points():
    return jsonify(ml_system.user_points)

@app.route('/api/ml-vertices')
def get_ml_vertices():
    return jsonify(ml_system.ml_vertices)

@app.route('/api/heatmap-data')
def get_heatmap_data():
    data = ml_system.get_heatmap_data()
    return jsonify(data)

@app.route('/api/ml-explanation')
def get_ml_explanation():
    explanation = ml_system.get_ml_explanation()
    return jsonify(explanation)

@app.route('/api/add-user-point', methods=['POST'])
def add_user_point():
    try:
        point_data = request.json
        new_point = ml_system.add_user_point(point_data)
        return jsonify({"status": "success", "point": new_point})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/generate-ml-polygons', methods=['POST'])
def generate_ml_polygons():
    try:
        result = ml_system.generate_ml_polygons()
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/export-combined')
def export_combined():
    try:
        # Crear archivo temporal para descarga
        with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as f:
            json.dump(ml_system.combined_data, f, indent=2)
            temp_path = f.name
        
        return send_file(temp_path, as_attachment=True, download_name='WildflowerBlooms_Combined.geojson')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/reset-database', methods=['POST'])
def reset_database():
    """Resetea la base de datos combinada a los datos originales"""
    try:
        # Recargar datos originales
        with open(ml_system.primary_geojson, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        ml_system.combined_data = original_data
        ml_system.save_combined_data()
        
        # Limpiar puntos de usuario
        ml_system.user_points = []
        ml_system.save_user_points()
        
        # Limpiar vértices ML
        ml_system.ml_vertices = []
        ml_system.save_ml_vertices()
        
        # Regenerar polígonos ML automáticamente después del reset
        ml_system.auto_generate_ml_polygons()
        
        return jsonify({"status": "success", "message": "Base de datos resetada a datos originales y polígonos ML regenerados"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("🚀 Inicializando Sistema ML de Wildflowers con EPS Automático...")
    ml_system = WildflowerMLSystem()
    app.run(debug=True, port=5000)
