import sys
import heapq
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox, QGraphicsView, QGraphicsScene,
    QSlider, QCheckBox, QInputDialog, QGraphicsEllipseItem, QGraphicsLineItem
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QAction, QIcon, QFont, QPen, QColor

class Grafo:
    def __init__(self, dirigido=True):
        self.dirigido = dirigido
        self.grafo = {}

    def agregar_nodo(self, nodo):
        if nodo not in self.grafo:
            self.grafo[nodo] = {}

    def agregar_arista(self, origen, destino, peso):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.grafo[origen][destino] = peso
        if not self.dirigido:
            self.grafo[destino][origen] = peso

    def dijkstra(self, inicio, fin):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        predecesores = {nodo: None for nodo in self.grafo}
        cola = [(0, inicio)]

        while cola:
            distancia_actual, nodo_actual = heapq.heappop(cola)

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.grafo[nodo_actual].items():
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        camino = []
        nodo = fin
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = predecesores[nodo]

        return distancias[fin], camino

class RouteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto - Cálculo de Ruta Más Corta")
        self.setGeometry(100, 100, 1200, 700)
        self.dark_mode = False
        self.grafo = Grafo(dirigido=True)
        self.node_positions = {}
        self.node_items = {}
        self.edge_items = []
        self.initUI()

    def initUI(self):
        toolbar = self.addToolBar("Opciones")
        toolbar.setMovable(False)

        toggle_theme = QAction(QIcon(), "Modo Oscuro/Claro", self)
        toggle_theme.triggered.connect(self.toggle_theme)
        toolbar.addAction(toggle_theme)

        container = QWidget()
        main_layout = QHBoxLayout()

        control_panel = QVBoxLayout()
        control_panel.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Cálculo de Ruta Más Corta")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        control_panel.addWidget(title)

        label_nodes = QLabel("Nodos y Aristas:")
        label_nodes.setFont(QFont("Segoe UI", 12))
        control_panel.addWidget(label_nodes)

        add_node_btn = QPushButton("Agregar Nodo")
        add_edge_btn = QPushButton("Agregar Arista")
        calculate_btn = QPushButton("Calcular Ruta Óptima")

        for b in (add_node_btn, add_edge_btn, calculate_btn):
            b.setMinimumHeight(40)
            b.setFont(QFont("Segoe UI", 11))
            control_panel.addWidget(b)

        add_node_btn.clicked.connect(self.on_add_node)
        add_edge_btn.clicked.connect(self.on_add_edge)
        calculate_btn.clicked.connect(self.on_calculate)

        origin_label = QLabel("Origen:")
        destination_label = QLabel("Destino:")
        self.origin_combo = QComboBox()
        self.destination_combo = QComboBox()

        control_panel.addWidget(origin_label)
        control_panel.addWidget(self.origin_combo)
        control_panel.addWidget(destination_label)
        control_panel.addWidget(self.destination_combo)

        zoom_label = QLabel("Zoom del Grafo:")
        zoom_slider = QSlider(Qt.Orientation.Horizontal)
        zoom_slider.setMinimum(1)
        zoom_slider.setMaximum(100)
        zoom_slider.setValue(50)
        control_panel.addWidget(zoom_label)
        control_panel.addWidget(zoom_slider)

        mode_toggle = QCheckBox("Modo Oscuro")
        mode_toggle.stateChanged.connect(self.toggle_theme)
        control_panel.addWidget(mode_toggle)

        self.graph_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graph_view.setScene(self.scene)
        main_layout.addLayout(control_panel, 2)
        main_layout.addWidget(self.graph_view, 5)

        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.apply_light_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: white; }
            QLabel { color: white; }
            QPushButton { background-color: #3a3a3a; color: white; border-radius: 6px; }
            QPushButton:hover { background-color: #505050; }
            QComboBox, QSlider, QCheckBox { color: white; background-color: #2b2b2b; }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f9f9f9; color: black; }
            QLabel { color: black; }
            QPushButton { background-color: #e0e0e0; color: black; border-radius: 6px; }
            QPushButton:hover { background-color: #d0d0d0; }
            QComboBox, QSlider, QCheckBox { color: black; background-color: white; }
        """)

    def on_add_node(self):
        text, ok = QInputDialog.getText(self, "Agregar Nodo", "Nombre del nodo:")
        if ok and text:
            nombre = text.strip()
            if nombre and nombre not in self.grafo.grafo:
                self.grafo.agregar_nodo(nombre)
                self.origin_combo.addItem(nombre)
                self.destination_combo.addItem(nombre)

                x, y = len(self.node_positions)*100 + 50, 300
                self.node_positions[nombre] = QPointF(x, y)
                node_item = self.scene.addEllipse(x, y, 40, 40, QPen(Qt.GlobalColor.black), QColor("skyblue"))
                text_item = self.scene.addText(nombre, QFont("Segoe UI", 10))
                text_item.setPos(x + 10, y + 10)
                self.node_items[nombre] = node_item

    def on_add_edge(self):
        if not self.grafo.grafo:
            QMessageBox.warning(self, "Sin nodos", "Agrega primero nodos antes de crear una arista.")
            return

        origen, ok1 = QInputDialog.getItem(self, "Agregar Arista", "Origen:", list(self.grafo.grafo.keys()), 0, False)
        if not ok1:
            return
        destino, ok2 = QInputDialog.getItem(self, "Agregar Arista", "Destino:", list(self.grafo.grafo.keys()), 0, False)
        if not ok2:
            return
        peso_text, ok3 = QInputDialog.getText(self, "Agregar Arista", "Peso (número):")
        if not ok3:
            return
        try:
            peso = float(peso_text)
        except ValueError:
            QMessageBox.warning(self, "Peso inválido", "Introduce un número válido para el peso.")
            return

        self.grafo.agregar_arista(origen, destino, peso)
        p1, p2 = self.node_positions[origen], self.node_positions[destino]
        line = self.scene.addLine(p1.x()+20, p1.y()+20, p2.x()+20, p2.y()+20, QPen(Qt.GlobalColor.black, 2))
        self.edge_items.append((origen, destino, line))

    def on_calculate(self):
        if not self.grafo.grafo:
            QMessageBox.warning(self, "Grafo vacío", "No hay nodos en el grafo.")
            return

        origen = self.origin_combo.currentText()
        destino = self.destination_combo.currentText()
        if origen == "" or destino == "":
            QMessageBox.warning(self, "Seleccione nodos", "Selecciona origen y destino.")
            return

        distancia, camino = self.grafo.dijkstra(origen, destino)
        if distancia == float('inf'):
            QMessageBox.information(self, "Sin ruta", f"No existe ruta de {origen} a {destino}.")
            return

        for _, _, line in self.edge_items:
            line.setPen(QPen(Qt.GlobalColor.black, 2))

        for i in range(len(camino) - 1):
            o, d = camino[i], camino[i+1]
            for orig, dest, line in self.edge_items:
                if (orig == o and dest == d) or (not self.grafo.dirigido and orig == d and dest == o):
                    line.setPen(QPen(QColor("red"), 4))

        QMessageBox.information(self, "Ruta encontrada", f"Distancia: {distancia}\nCamino: {' -> '.join(camino)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RouteApp()
    window.show()
    sys.exit(app.exec())
