import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, QMessageBox,
    QGraphicsView, QGraphicsScene, QSlider, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QFont

class RouteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto - Cálculo de Ruta Más Corta")
        self.setGeometry(100, 100, 1200, 700)

        self.dark_mode = False
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

        graph_view = QGraphicsView()
        self.scene = QGraphicsScene()
        graph_view.setScene(self.scene)
        graph_view.setRenderHint(graph_view.renderHints())

        main_layout.addLayout(control_panel, 2)
        main_layout.addWidget(graph_view, 5)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RouteApp()
    window.show()
    sys.exit(app.exec())
