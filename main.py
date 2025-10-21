import sys
import heapq
import math
from collections import deque, defaultdict
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox, QGraphicsView, QGraphicsScene,
    QSlider, QCheckBox, QInputDialog, QSpinBox
)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QFont, QPen, QColor, QBrush, QTransform, QPainter

NODE_R = 22

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
        distancias = {n: float('inf') for n in self.grafo}
        distancias[inicio] = 0
        predecesores = {n: None for n in self.grafo}
        cola = [(0, inicio)]
        while cola:
            d, u = heapq.heappop(cola)
            if d > distancias[u]:
                continue
            for v, w in self.grafo[u].items():
                nd = d + w
                if nd < distancias[v]:
                    distancias[v] = nd
                    predecesores[v] = u
                    heapq.heappush(cola, (nd, v))
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
        self.edges_data = []
        self.ui_font_size = 11
        self.title_font_size = 20
        self.node_font_size = 10
        self.weight_font_size = 9
        self.initUI()

    def initUI(self):
        container = QWidget()
        main_layout = QHBoxLayout()

        control_panel = QVBoxLayout()
        control_panel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel("Cálculo de Ruta Más Corta")
        self.title.setFont(QFont("Segoe UI", self.title_font_size, QFont.Weight.Bold))
        control_panel.addWidget(self.title)

        self.label_nodes = QLabel("Nodos y Aristas:")
        self.label_nodes.setFont(QFont("Segoe UI", 12))
        control_panel.addWidget(self.label_nodes)

        self.add_node_btn = QPushButton("Agregar Nodo")
        self.add_edge_btn = QPushButton("Agregar Arista")
        self.calculate_btn = QPushButton("Calcular Ruta Óptima")
        for b in (self.add_node_btn, self.add_edge_btn, self.calculate_btn):
            b.setMinimumHeight(40)
            b.setFont(QFont("Segoe UI", self.ui_font_size))
            control_panel.addWidget(b)
        self.add_node_btn.clicked.connect(self.on_add_node)
        self.add_edge_btn.clicked.connect(self.on_add_edge)
        self.calculate_btn.clicked.connect(self.on_calculate)

        self.origin_label = QLabel("Origen:")
        self.destination_label = QLabel("Destino:")
        self.origin_combo = QComboBox()
        self.destination_combo = QComboBox()
        control_panel.addWidget(self.origin_label)
        control_panel.addWidget(self.origin_combo)
        control_panel.addWidget(self.destination_label)
        control_panel.addWidget(self.destination_combo)

        zoom_row = QHBoxLayout()
        zoom_lbl = QLabel("Zoom:")
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(20)
        self.zoom_slider.setMaximum(300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.on_zoom_change)
        zoom_row.addWidget(zoom_lbl)
        zoom_row.addWidget(self.zoom_slider)
        control_panel.addLayout(zoom_row)

        font_row = QHBoxLayout()
        font_lbl = QLabel("Tamaño texto:")
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 28)
        self.font_spin.setValue(self.ui_font_size)
        self.font_spin.valueChanged.connect(self.on_font_change)
        font_row.addWidget(font_lbl)
        font_row.addWidget(self.font_spin)
        control_panel.addLayout(font_row)

        self.mode_toggle = QCheckBox("Modo Oscuro")
        self.mode_toggle.stateChanged.connect(self.toggle_theme)
        control_panel.addWidget(self.mode_toggle)

        self.path_label = QLabel("Ruta: —")
        self.path_label.setWordWrap(True)
        self.path_label.setFont(QFont("Segoe UI", self.ui_font_size))
        control_panel.addWidget(self.path_label)

        self.graph_view = QGraphicsView()
        self.graph_view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.scene = QGraphicsScene()
        self.graph_view.setScene(self.scene)
        self.scene.setBackgroundBrush(QBrush(QColor("#fefefe")))

        main_layout.addLayout(control_panel, 2)
        main_layout.addWidget(self.graph_view, 5)

        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.apply_light_theme()

    def on_font_change(self, val):
        self.ui_font_size = val
        self.node_font_size = max(8, val - 1)
        self.weight_font_size = max(8, val - 2)
        self.apply_font_sizes()
        self.draw_graph()

    def apply_font_sizes(self):
        self.title.setFont(QFont("Segoe UI", max(self.ui_font_size+8, 16), QFont.Weight.Bold))
        self.label_nodes.setFont(QFont("Segoe UI", self.ui_font_size))
        self.origin_label.setFont(QFont("Segoe UI", self.ui_font_size))
        self.destination_label.setFont(QFont("Segoe UI", self.ui_font_size))
        self.add_node_btn.setFont(QFont("Segoe UI", self.ui_font_size))
        self.add_edge_btn.setFont(QFont("Segoe UI", self.ui_font_size))
        self.calculate_btn.setFont(QFont("Segoe UI", self.ui_font_size))
        self.path_label.setFont(QFont("Segoe UI", self.ui_font_size))
        self.origin_combo.setFont(QFont("Segoe UI", self.ui_font_size))
        self.destination_combo.setFont(QFont("Segoe UI", self.ui_font_size))

    def on_zoom_change(self, value):
        factor = value / 100.0
        t = QTransform()
        t.scale(factor, factor)
        self.graph_view.setTransform(t)

    def toggle_theme(self):
        self.dark_mode = self.mode_toggle.isChecked()
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
        self.draw_graph()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: white; }
            QLabel { color: white; }
            QPushButton { background-color: #3a3a3a; color: white; border-radius: 6px; }
            QPushButton:hover { background-color: #505050; }
            QComboBox, QSlider, QCheckBox { color: white; background-color: #2b2b2b; }
            QSpinBox { color: white; background-color: #2b2b2b; }
        """)
        self.scene.setBackgroundBrush(QBrush(QColor("#2b2b2b")))

    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f7f7f7; color: #111; }
            QLabel { color: #111; }
            QPushButton { background-color: #e4e4e4; color: #111; border-radius: 6px; }
            QPushButton:hover { background-color: #d0d0d0; }
            QComboBox, QSlider, QCheckBox { color: #111; background-color: #ffffff; }
            QSpinBox { color: #111; background-color: #ffffff; }
        """)
        self.scene.setBackgroundBrush(QBrush(QColor("#fefefe")))

    def on_add_node(self):
        text, ok = QInputDialog.getText(self, "Agregar Nodo", "Nombre del nodo:")
        if ok and text:
            nombre = text.strip()
            if nombre and nombre not in self.grafo.grafo:
                self.grafo.agregar_nodo(nombre)
                self.origin_combo.addItem(nombre)
                self.destination_combo.addItem(nombre)
                self.layout_tree()
                self.draw_graph()

    def on_add_edge(self):
        if not self.grafo.grafo:
            QMessageBox.warning(self, "Sin nodos", "Agrega primero nodos antes de crear una arista.")
        else:
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
            self.edges_data.append((origen, destino, peso))
            self.layout_tree()
            self.draw_graph()

    def on_calculate(self):
        if not self.grafo.grafo:
            QMessageBox.warning(self, "Grafo vacío", "No hay nodos en el grafo.")
            return
        origen = self.origin_combo.currentText()
        destino = self.destination_combo.currentText()
        if not origen or not destino:
            QMessageBox.warning(self, "Seleccione nodos", "Selecciona origen y destino.")
            return
        distancia, camino = self.grafo.dijkstra(origen, destino)
        if distancia == float('inf') or len(camino) == 0:
            QMessageBox.information(self, "Sin ruta", f"No existe ruta de {origen} a {destino}.")
            return
        self.path_label.setText(f"Ruta: {' -> '.join(camino)}  |  Distancia: {distancia}")
        self.draw_graph(highlight_path=camino)

    def layout_tree(self):
        self.node_positions.clear()
        if not self.grafo.grafo:
            return
        root = self.origin_combo.currentText() if self.origin_combo.count() else None
        if not root:
            root = next(iter(self.grafo.grafo))
        niveles = defaultdict(list)
        visited = set()
        cola = deque([root])
        visited.add(root)
        depth = {root: 0}
        while cola:
            u = cola.popleft()
            niveles[depth[u]].append(u)
            vecinos = list(self.grafo.grafo[u].keys())
            if not self.grafo.dirigido:
                for x in self.grafo.grafo:
                    if u in self.grafo.grafo[x]:
                        if x not in vecinos:
                            vecinos.append(x)
            for v in vecinos:
                if v not in visited:
                    visited.add(v)
                    depth[v] = depth[u] + 1
                    cola.append(v)
        for n in self.grafo.grafo:
            if n not in visited:
                visited.add(n)
                depth[n] = max(depth.values()) + 1 if depth else 0
                niveles[depth[n]].append(n)
        lvl_keys = sorted(niveles.keys())
        vgap = 120
        hgap = 140
        width = max(800, self.graph_view.width())
        for i, lvl in enumerate(lvl_keys):
            nodes_at_lvl = niveles[lvl]
            count = len(nodes_at_lvl)
            total_width = (count - 1) * hgap
            start_x = (width - total_width) / 2
            y = 80 + i * vgap
            for j, n in enumerate(nodes_at_lvl):
                x = start_x + j * hgap
                self.node_positions[n] = QPointF(x, y)

    def draw_graph(self, highlight_path=None):
        self.scene.clear()
        bg = QColor("#2b2b2b") if self.dark_mode else QColor("#fefefe")
        self.scene.setBackgroundBrush(QBrush(bg))
        base_edge_color = QColor("white") if self.dark_mode else QColor("#111")
        text_color = QColor("white") if self.dark_mode else QColor("#111")
        for (u, v, w) in self.edges_data:
            if u not in self.node_positions or v not in self.node_positions:
                continue
            self._draw_arrow(self.node_positions[u], self.node_positions[v], base_edge_color, 2, 1)
            mx = (self.node_positions[u].x() + self.node_positions[v].x())/2 + NODE_R
            my = (self.node_positions[u].y() + self.node_positions[v].y())/2 + NODE_R
            rect = QRectF(mx-12, my-10, 28, 18)
            bg_brush = QBrush(QColor(255,255,255,60) if not self.dark_mode else QColor(0,0,0,80))
            self.scene.addRect(rect, QPen(Qt.PenStyle.NoPen), bg_brush)
            wt = self.scene.addText(str(w), QFont("Segoe UI", self.weight_font_size))
            wt.setDefaultTextColor(text_color)
            wt.setPos(mx-8, my-9)
            wt.setZValue(3)
        path_edges = set()
        if highlight_path and len(highlight_path) > 1:
            for i in range(len(highlight_path)-1):
                path_edges.add((highlight_path[i], highlight_path[i+1]))
        for (u, v, w) in self.edges_data:
            if (u, v) in path_edges or (not self.grafo.dirigido and (v, u) in path_edges):
                self._draw_arrow(self.node_positions[u], self.node_positions[v], QColor("#ff3333"), 4, 5)
        for n, pos in self.node_positions.items():
            pen = QPen(QColor("#111") if not self.dark_mode else QColor("#eaeaea"))
            brush = QBrush(QColor("#66b2ff") if not self.dark_mode else QColor("#3399ff"))
            circ = self.scene.addEllipse(pos.x(), pos.y(), NODE_R*2, NODE_R*2, pen, brush)
            circ.setZValue(10)
            txt = self.scene.addText(n, QFont("Segoe UI", self.node_font_size))
            txt.setDefaultTextColor(text_color)
            txt.setPos(pos.x()+8, pos.y()+6)
            txt.setZValue(11)

    def _draw_arrow(self, center1, center2, color, thickness, z):
        x1, y1 = center1.x()+NODE_R, center1.y()+NODE_R
        x2, y2 = center2.x()+NODE_R, center2.y()+NODE_R
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L == 0:
            return
        ux, uy = dx / L, dy / L
        sx, sy = x1 + ux * NODE_R, y1 + uy * NODE_R
        ex, ey = x2 - ux * NODE_R, y2 - uy * NODE_R
        pen = QPen(color, thickness)
        line = self.scene.addLine(sx, sy, ex, ey, pen)
        line.setZValue(z)
        head_len = 14
        head_ang = math.radians(28)
        angle = math.atan2(ey - sy, ex - sx)
        lx = ex - head_len * math.cos(angle - head_ang)
        ly = ey - head_len * math.sin(angle - head_ang)
        rx = ex - head_len * math.cos(angle + head_ang)
        ry = ey - head_len * math.sin(angle + head_ang)
        l1 = self.scene.addLine(ex, ey, lx, ly, pen)
        l2 = self.scene.addLine(ex, ey, rx, ry, pen)
        l1.setZValue(z)
        l2.setZValue(z)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RouteApp()
    window.show()
    sys.exit(app.exec())
