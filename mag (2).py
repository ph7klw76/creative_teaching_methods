# -*- coding: utf-8 -*-

import sys
import numpy as np

# --- Matplotlib Setup (Attempt backend setting early) ---
MATPLOTLIB_AVAILABLE = True # Assume not available initially
try:
    import matplotlib
    matplotlib.use('Qt5Agg') # Set the backend for PyQt5 compatibility
    MATPLOTLIB_AVAILABLE = True
    print("Matplotlib found and backend set to Qt5Agg.")
except ImportError:
    print("Warning: Matplotlib library not found. Plots will be disabled.")

# --- PyQt5 Imports (MUST come after backend setting if using matplotlib) ---
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel,
                             QTabWidget, QGridLayout, QSizePolicy, QFrame, QRadioButton, QButtonGroup,
                             QPushButton, QSpacerItem)
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF, QFont, QPalette
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF, pyqtSignal, QObject

# --- Matplotlib Imports (conditional based on earlier check) ---
if MATPLOTLIB_AVAILABLE:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.ticker as mticker

    # --- Define the REAL MplCanvas using Matplotlib ---
    class MplCanvas(FigureCanvas):
        """Matplotlib Canvas widget for embedding plots in PyQt."""
        def __init__(self, parent=None, width=5, height=4, dpi=100):
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = self.fig.add_subplot(111)
            super().__init__(self.fig)
            self.setParent(parent)
            # Set Qt size policies
            FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
            # Ensure tight layout is applied to the figure
            self.figure.set_tight_layout(True)
else:
    # --- Define a PLACEHOLDER MplCanvas if Matplotlib is missing ---
    class MplCanvas(QWidget):
        """Placeholder widget displayed when Matplotlib is not installed."""
        axes = None # Dummy attribute expected by update methods

        class DummyFigure: # Nested dummy class for the 'figure' attribute
            def tight_layout(self, *args, **kwargs): pass # Dummy method

        figure = DummyFigure() # Assign dummy figure instance

        def __init__(self, parent=None, width=5, height=4, dpi=100):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Matplotlib not installed.\nPlotting is disabled.")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-style: italic; color: gray;")
            layout.addWidget(label)
            # Set minimum size to prevent collapsing completely
            self.setMinimumSize(int(width*dpi*0.7), int(height*dpi*0.7))
            print("Created placeholder MplCanvas.")

        def draw(self):
            """Dummy draw method, does nothing."""
            pass


# =============================================================================
# Constants
# =============================================================================
SPIN_ARROW_LENGTH = 25      # Visual length of spin arrows
SPIN_ARROW_HEAD_SIZE = 6    # Size of arrowhead polygon
GRID_SPACING = 40           # Default visual spacing for lattices/walls
UPDATE_INTERVAL = 40        # Animation timer interval in milliseconds
PI = np.pi                  # Mathematical constant pi

# =============================================================================
# Helper Functions
# =============================================================================
def create_arrowhead(end_point, direction_vector, size):
    """Creates a QPolygonF representing an arrowhead."""
    norm = np.linalg.norm(direction_vector)
    if norm < 1e-9: norm_dir = np.array([1.0, 0.0])
    else: norm_dir = direction_vector / norm
    perp_vec = np.array([-norm_dir[1], norm_dir[0]])
    p1 = end_point
    p2 = end_point - norm_dir * size + perp_vec * size / 2
    p3 = end_point - norm_dir * size - perp_vec * size / 2
    return QPolygonF([QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]), QPointF(p3[0], p3[1])])

# =============================================================================
# Helper Classes
# =============================================================================
class UpdateNotifier(QObject):
    """Simple QObject to emit a signal when an update is needed."""
    updated = pyqtSignal()

# =============================================================================
# Custom Widgets Base Class
# =============================================================================
class SpinWidget(QWidget):
    """Base class for widgets that draw spins."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._background_color = QColor(Qt.white)

    def setBackgroundColor(self, color):
        self._background_color = QColor(color)
        palette = self.palette()
        palette.setColor(QPalette.Window, self._background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self._background_color)
        self.draw_spins(painter)

    def draw_spins(self, painter): pass # Implemented by subclasses

# =============================================================================
# Tab 1: Two-Spin Heisenberg Widget
# =============================================================================
class TwoSpinWidget(SpinWidget):
    """Widget to visualize the interaction between two spins."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.s1_angle = 0
        self.s2_angle_rad = 0
        self.J = 1.0 
        self.S = 1.0
        self.animating = False
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_step)
        self.animation_angle_target = np.pi
        self.animation_speed = 0.05

    def set_j(self, value): 
        self.J = value 
        self.update()
        
    def set_s(self, value): 
        self.S = value 
        self.update()
        
    def set_s2_angle_deg(self, degrees):
        if not self.animating: 
            self.s2_angle_rad = np.radians(degrees)
            self.update()
            
    def get_energy(self, theta_rad):
        safe_J = self.J if abs(self.J) > 1e-9 else 1e-9
        return -safe_J * (self.S**2) * np.cos(theta_rad)
    
    def start_animation(self, target_angle_rad):
        self.animation_angle_target = target_angle_rad
        self.animating = True
        self.animation_timer.start(UPDATE_INTERVAL)
        
    def stop_animation(self):
        self.animating = False 
        self.animation_timer.stop()
        
    def animate_step(self):
        diff = self.animation_angle_target - self.s2_angle_rad
        while diff <= -np.pi: diff += 2 * np.pi
        while diff > np.pi: diff -= 2 * np.pi
        step = np.sign(diff) * min(abs(diff), self.animation_speed)
        energy_now = self.get_energy(self.s2_angle_rad)
        energy_next = self.get_energy(self.s2_angle_rad + step)
        energy_gradient_factor = 1.0 + 2.0 * max(0, (energy_now - energy_next) / abs(energy_now + 1e-6))
        effective_step = step * energy_gradient_factor
        self.s2_angle_rad += effective_step 
        self.s2_angle_rad = self.s2_angle_rad % (2 * np.pi)
        self.update()
        if abs(diff) < self.animation_speed / 2 :
            self.s2_angle_rad = self.animation_angle_target
            self.stop_animation()
            self.update()
            
    def draw_spins(self, painter):
        w, h = self.width(), self.height()
        center_x, center_y = w / 2, h / 2
        separation = SPIN_ARROW_LENGTH * 1.5
        # Spin 1
        s1_start = np.array([center_x - separation / 2, center_y])
        s1_end = s1_start + np.array([SPIN_ARROW_LENGTH, 0])
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.black))
        painter.drawLine(int(s1_start[0]), int(s1_start[1]), int(s1_end[0]), int(s1_end[1]))
        painter.drawPolygon(create_arrowhead(s1_end, np.array([1, 0]), SPIN_ARROW_HEAD_SIZE))
        painter.drawText(int(s1_start[0] - 20), int(s1_start[1] + 20), "S₁")
        
        # Spin 2
        s2_start = np.array([center_x + separation / 2, center_y])
        s2_dir = np.array([np.cos(self.s2_angle_rad), np.sin(self.s2_angle_rad)])
        s2_end = s2_start + s2_dir * SPIN_ARROW_LENGTH
        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(QBrush(Qt.red))
        painter.drawLine(int(s2_start[0]), int(s2_start[1]), int(s2_end[0]), int(s2_end[1]))
        painter.drawPolygon(create_arrowhead(s2_end, s2_dir, SPIN_ARROW_HEAD_SIZE))
        painter.drawText(int(s2_start[0] + 10), int(s2_start[1] + 20), "S₂")
        # Angle Arc
        angle_deg = np.degrees(self.s2_angle_rad)
        rect_size = SPIN_ARROW_LENGTH * 1.2
        rect = QRectF(s2_start[0] - rect_size/2, s2_start[1] - rect_size/2, rect_size, rect_size)
        painter.setPen(QPen(Qt.blue, 1, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect.toRect(), 0 * 16, int(angle_deg * 16))
        theta_text = f"θ = {angle_deg:.1f}°"
        label_angle = self.s2_angle_rad / 2
        label_radius = rect_size * 0.6
        label_pos_x = s2_start[0] + label_radius * np.cos(label_angle)
        label_pos_y = s2_start[1] + label_radius * np.sin(label_angle)
        painter.setPen(Qt.blue)
        painter.drawText(int(label_pos_x), int(label_pos_y), theta_text)
        # Energy Label
        energy = self.get_energy(self.s2_angle_rad)
        energy_text = f"E(θ) = {energy:.2f} (arb. units)"
        painter.setPen(Qt.darkGreen)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(10, h - 15, energy_text)
        # Ground State Text
        ground_state_text = ""
        pen_color = Qt.gray
        if self.J > 0: 
            ground_state_text = "J > 0: Ferromagnetic (FM) ground state (θ = 0°)"
            pen_color = Qt.darkMagenta
        elif self.J < 0: 
            ground_state_text = "J < 0: Antiferromagnetic (AFM) ground state (θ = 180°)"
            pen_color = Qt.darkCyan
        else: ground_state_text = "J = 0: No interaction"
        painter.setPen(QPen(pen_color))
        painter.drawText(10, 25, ground_state_text)

# =============================================================================
# Tab 2: Spin Chain Wave Widget
# =============================================================================
class SpinChainWidget(SpinWidget):
    """Widget to visualize a spin wave propagating along a 1D chain."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.num_spins = 20
        self.a_pixels = GRID_SPACING
        self.k_val = 0.0
        self.omega_val = 0.0
        self.time = 0.0
        self.animating = False
        self.spin_color = QColor(Qt.blue)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_step)
        self.setBackgroundColor(QColor("#F0FFF0"))
        self.setMinimumHeight(80)

    def set_params(self, k, omega, a_pixels):
        self.k_val = k
        self.omega_val = omega
        self.a_pixels = a_pixels
        self.update()
        
    def start_animation(self):
        if not self.animating:
            self.time = 0.0
            self.animating = True
            self.animation_timer.start(UPDATE_INTERVAL)
            
    def stop_animation(self):
        if self.animating:
            self.animating = False
            self.animation_timer.stop()
            self.update()
            
    def animate_step(self):
        time_scale_factor = 0.5
        self.time += (UPDATE_INTERVAL / 1000.0) * self.omega_val * time_scale_factor
        self.update()
        
    def draw_spins(self, painter):
        w, h = self.width(), self.height()
        center_y = h / 2
        total_width = self.num_spins * self.a_pixels
        start_x = (w - total_width) / 2
        painter.setPen(QPen(self.spin_color, 2))
        painter.setBrush(QBrush(self.spin_color))
        max_angle_deviation = PI / 4
        for i in range(self.num_spins):
            x_pos_visual = start_x + i * self.a_pixels
            phase = self.k_val * x_pos_visual - self.time if self.animating else self.k_val * x_pos_visual
            angle_deviation = max_angle_deviation * np.cos(phase)
            spin_angle_rad = -PI/2 + angle_deviation
            spin_start = np.array([x_pos_visual, center_y])
            spin_dir = np.array([np.cos(spin_angle_rad), np.sin(spin_angle_rad)])
            spin_end = spin_start + spin_dir * SPIN_ARROW_LENGTH
            painter.drawLine(int(spin_start[0]), int(spin_start[1]), int(spin_end[0]), int(spin_end[1]))
            painter.drawPolygon(create_arrowhead(spin_end, spin_dir, SPIN_ARROW_HEAD_SIZE))

# =============================================================================
# Tab 3: Domain Wall Visualization Widget
# =============================================================================
class DomainWallWidget(SpinWidget):
    """Widget to visualize the spin rotation across a domain wall."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.num_spins = 25
        self.delta_w_pixels = 5 * GRID_SPACING
        self.x_range_factor = 3.0
        self.spin_color_left = QColor(Qt.darkGreen)
        self.spin_color_right = QColor(Qt.darkRed)
        self.spin_color_wall = QColor(Qt.darkBlue)
        self.setBackgroundColor(QColor("#FFF0F5")) 
        self.setMinimumHeight(80)

    def set_delta_w(self, delta_w_pixels):
        self.delta_w_pixels = max(delta_w_pixels, GRID_SPACING / 5.0)
        self.update()
        
    def draw_spins(self, painter):
        w, h = self.width(), self.height()
        center_x, center_y = w / 2, h / 2
        total_visual_width = self.x_range_factor * 2 * self.delta_w_pixels
        spin_spacing = total_visual_width / max(1, self.num_spins -1) if self.num_spins > 1 else total_visual_width
        start_x = center_x - total_visual_width / 2
        painter.setPen(QPen(Qt.black, 1))
        for i in range(self.num_spins):
            x_pos_visual = start_x + i * spin_spacing
            x_relative = x_pos_visual - center_x
            x_norm = x_relative / self.delta_w_pixels if self.delta_w_pixels > 1e-6 else x_relative * 1e6
            mz = np.tanh(x_norm)
            my = 1.0 / np.cosh(x_norm)
            pen_color = self.spin_color_wall
            brush_color = self.spin_color_wall
            if abs(x_norm) >= 1.0:
                 if x_norm <= -1.0: 
                     pen_color = self.spin_color_left
                     brush_color = self.spin_color_left
                 else: pen_color = self.spin_color_right
                 brush_color = self.spin_color_right
            painter.setPen(QPen(pen_color, 2))
            painter.setBrush(QBrush(brush_color))
            spin_start = np.array([x_pos_visual, center_y])
            spin_dir = np.array([my, -mz])
            spin_end = spin_start + spin_dir * SPIN_ARROW_LENGTH
            painter.drawLine(int(spin_start[0]), int(spin_start[1]), int(spin_end[0]), int(spin_end[1]))
            painter.drawPolygon(create_arrowhead(spin_end, spin_dir, SPIN_ARROW_HEAD_SIZE))
        # Draw dashed lines
        # --- Draw Domain Wall Width Indicators ---
        painter.setPen(QPen(Qt.gray, 1, Qt.DashLine))
        # Line at the center of the wall (cast potential float center_x)
        painter.drawLine(int(center_x), 10, int(center_x), h - 10)
        # Lines indicating the boundaries +/- delta_w
        boundary_left_x = center_x - self.delta_w_pixels
        boundary_right_x = center_x + self.delta_w_pixels
        tick_height = 15
        # CORRECTED: Cast float results (center_y +/- tick_height) to int
        painter.drawLine(int(boundary_left_x), int(center_y - tick_height), int(boundary_left_x), int(center_y + tick_height))
        painter.drawLine(int(boundary_right_x), int(center_y - tick_height), int(boundary_right_x), int(center_y + tick_height))
        # Labels for the boundaries (ensure position is int)
        # Cast center_y used in text positioning as well
        painter.drawText(int(boundary_left_x - 10), int(center_y - tick_height - 5), "-δw")
        painter.drawText(int(boundary_right_x - 5), int(center_y - tick_height - 5), "+δw")

# =============================================================================
# Main Application Window
# =============================================================================
class ExchangeAnimator(QMainWindow):
    """Main application window holding the tabs and controls."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exchange Interaction Animator")
        self.setGeometry(50, 50, 1150, 900)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        # Create tabs
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "1. Discrete Heisenberg")
        self.setup_tab1()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "2. Magnon Dispersion (1D)")
        self.setup_tab2()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "3. Continuum (Domain Wall)")
        self.setup_tab3()
        self.apply_stylesheet() # Apply styles after widgets are created

    def apply_stylesheet(self):
        """Applies CSS-like styles to the application widgets."""
        # Includes increased font sizes and padding
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QWidget { font-size: 11pt; }
            QTabWidget::pane { border-top: 2px solid #C2C7CB; background-color: white; }
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 1px solid #C4C4C3; border-bottom-color: #C2C7CB; border-top-left-radius: 4px; border-top-right-radius: 4px;
                min-width: 12ex; padding: 7px; margin-right: 2px;
            }
            QTabBar::tab:selected { background: white; border-color: #9B9B9B; border-bottom-color: white; }
            QTabBar::tab:!selected:hover { background: #e0e0e0; }
            QFrame#controlsFrame { border: 1px solid #c0c0c0; border-radius: 5px; background-color: #fafafa; padding: 10px; margin-top: 10px; }
            QFrame#infoFrame { border: 1px solid #d0d0d0; border-radius: 5px; background-color: #f8f8ff; padding: 12px; }
            QLabel { padding-bottom: 4px; }
            QLabel#titleLabel { font-size: 18pt; font-weight: bold; color: #0050a0; margin-bottom: 15px; padding-bottom: 5px; }
            QLabel#descLabel { font-size: 12pt; line-height: 1.3; }
            QLabel#eqLabel { font-family: "Consolas", "Courier New", monospace; font-size: 12pt; background-color: #e8e8f0; border: 1px solid #cccccc; border-radius: 3px; padding: 8px; margin-top: 6px; margin-bottom: 12px; text-align: center; }
            QTextBrowser#infoBrowser { background-color: #f8f8ff; border: 1px solid #d0d0d0; border-radius: 5px; }
            QSlider::groove:horizontal { height: 10px; background: #ddd; border-radius: 5px; }
            QSlider::handle:horizontal { background: #5a9; border: 1px solid #488; width: 18px; margin: -4px 0; border-radius: 9px; }
            QPushButton { padding: 8px 14px; border: 1px solid #bbb; border-radius: 4px; background-color: #e8e8e8; }
            QPushButton:hover { background-color: #d8d8d8; }
            QPushButton:pressed { background-color: #c8c8c8; }
            QDoubleSpinBox { padding: 4px; border: 1px solid #ccc; border-radius: 3px; }
            QRadioButton { margin-right: 15px; } QCheckBox { margin-right: 15px; }
        """)

    # --- Tab Setup Methods ---
    def setup_tab1(self):
        """Sets up the layout and widgets for Tab 1 (Two-Spin Heisenberg)."""
        layout = QHBoxLayout(self.tab1)
        controls_layout = QVBoxLayout()
        vis_layout = QVBoxLayout()
        # Info Frame
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        title_label = QLabel("Discrete Heisenberg Model (Two Spins)")
        title_label.setObjectName("titleLabel")
        desc_label = QLabel("Describes <b>exchange interaction</b> between two spins <b>S</b>₁ and <b>S</b>₂. Strength given by <b>J</b>.")
        desc_label.setWordWrap(True)
        desc_label.setObjectName("descLabel")
        eq1_label = QLabel("H<sub>ex</sub> = - J (<b>S</b>₁ ⋅ <b>S</b>₂)")
        eq1_label.setObjectName("eqLabel")
        eq1_label.setAlignment(Qt.AlignCenter)
        desc_label2 = QLabel("If S₁ fixed, S₂ rotates by θ, |S₁|=|S₂|=S, energy is:")
        desc_label2.setWordWrap(True)
        desc_label2.setObjectName("descLabel")
        eq2_label = QLabel("E(θ) = -J S² cos(θ)")
        eq2_label.setObjectName("eqLabel")
        eq2_label.setAlignment(Qt.AlignCenter)
        desc_label3 = QLabel("• <b>J > 0 (FM):</b> Min energy at θ=0° (<b>parallel</b>).<br>• <b>J < 0 (AFM):</b> Min energy at θ=180° (<b>antiparallel</b>).<br>• <b>S:</b> Scales energy.<br><i>Animation shows S₂ relaxing to minimum energy.</i>")
        desc_label3.setWordWrap(True)
        desc_label3.setObjectName("descLabel")
        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)
        info_layout.addWidget(eq1_label)
        info_layout.addWidget(desc_label2)
        info_layout.addWidget(eq2_label)
        info_layout.addWidget(desc_label3)
        info_layout.addStretch()
        # Visualization Area
        self.two_spin_widget = TwoSpinWidget()
        self.two_spin_widget.setBackgroundColor(QColor("#E0F2F7"))
        vis_layout.addWidget(self.two_spin_widget, 3)
        # Use the MplCanvas class (either real or placeholder)
        self.energy_plot_canvas = MplCanvas(self, width=5, height=2.5, dpi=100)
        vis_layout.addWidget(self.energy_plot_canvas, 2)
        self.update_energy_plot() # Call update even for placeholder (does nothing if placeholder)
        # Controls Frame
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_group_layout = QGridLayout(controls_frame)
        controls_group_layout.setSpacing(12)
        self.j_label = QLabel()
        controls_group_layout.addWidget(self.j_label, 0, 0, 1, 2)
        self.j_slider = QSlider(Qt.Horizontal)
        self.j_slider.setMinimum(-200)
        self.j_slider.setMaximum(200)
        self.j_slider.setValue(int(self.two_spin_widget.J * 100))
        self.j_slider.valueChanged.connect(self.on_j_slider_change)
        controls_group_layout.addWidget(self.j_slider, 1, 0, 1, 2)
        j_sign_group = QButtonGroup(self)
        fm_radio = QRadioButton("Force J > 0 (FM)")
        afm_radio = QRadioButton("Force J < 0 (AFM)")
        fm_radio.setObjectName("fm_radio")
        afm_radio.setObjectName("afm_radio")
        fm_radio.setChecked(self.two_spin_widget.J > 0)
        afm_radio.setChecked(self.two_spin_widget.J < 0)
        fm_radio.toggled.connect(lambda checked: self.set_j_sign(1) if checked else None)
        afm_radio.toggled.connect(lambda checked: self.set_j_sign(-1) if checked else None)
        j_sign_group.addButton(fm_radio)
        j_sign_group.addButton(afm_radio)
        controls_group_layout.addWidget(fm_radio, 2, 0)
        controls_group_layout.addWidget(afm_radio, 2, 1)
        self.s_label = QLabel()
        controls_group_layout.addWidget(self.s_label, 3, 0, 1, 2)
        self.s_slider = QSlider(Qt.Horizontal)
        self.s_slider.setMinimum(5)
        self.s_slider.setMaximum(50)
        self.s_slider.setValue(int(self.two_spin_widget.S * 10))
        self.s_slider.valueChanged.connect(self.on_s_slider_change)
        controls_group_layout.addWidget(self.s_slider, 4, 0, 1, 2)
        s_info = QLabel("<i>(S scales energy magnitude)</i>")
        s_info.setStyleSheet("color: gray;")
        controls_group_layout.addWidget(s_info, 5, 0, 1, 2)
        self.theta_label = QLabel()
        controls_group_layout.addWidget(self.theta_label, 6, 0, 1, 2)
        self.theta_slider = QSlider(Qt.Horizontal)
        self.theta_slider.setMinimum(0)
        self.theta_slider.setMaximum(360)
        self.theta_slider.setValue(int(np.degrees(self.two_spin_widget.s2_angle_rad)))
        self.theta_slider.valueChanged.connect(self.on_theta_slider_change)
        controls_group_layout.addWidget(self.theta_slider, 7, 0, 1, 2)
        animate_button_layout = QHBoxLayout()
        self.animate_fm_button = QPushButton("Animate FM")
        self.animate_afm_button = QPushButton("Animate AFM")
        self.stop_anim_button = QPushButton("Stop")
        self.animate_fm_button.setToolTip("Animate to Ferromagnetic Ground State (θ=0°)")
        self.animate_afm_button.setToolTip("Animate to Antiferromagnetic Ground State (θ=180°)")
        self.stop_anim_button.setToolTip("Stop Animation")
        self.animate_fm_button.clicked.connect(lambda: self.start_two_spin_animation(0))
        self.animate_fm_button.setStyleSheet("background-color: #C8E6C9;")
        self.animate_afm_button.clicked.connect(lambda: self.start_two_spin_animation(np.pi))
        self.animate_afm_button.setStyleSheet("background-color: #FFCDD2;")
        self.stop_anim_button.clicked.connect(self.two_spin_widget.stop_animation)
        self.stop_anim_button.setStyleSheet("background-color: #CFD8DC;")
        animate_button_layout.addWidget(self.animate_fm_button)
        animate_button_layout.addWidget(self.animate_afm_button)
        animate_button_layout.addWidget(self.stop_anim_button)
        controls_group_layout.addLayout(animate_button_layout, 8, 0, 1, 2)
        controls_group_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 9, 0)
        # Assemble Layouts
        controls_layout.addWidget(info_frame, 2)
        controls_layout.addWidget(controls_frame, 3)
        layout.addLayout(vis_layout, 7)
        layout.addLayout(controls_layout, 5)
        # Connect Signals
        self.two_spin_widget.update_signal = UpdateNotifier()
        self.setup_spin_widget_update_signal(self.two_spin_widget)
        self.two_spin_widget.update_signal.updated.connect(self.update_energy_plot)
        self.two_spin_widget.update_signal.updated.connect(self.update_tab1_labels)
        self.update_tab1_labels() # Initial update

    def setup_tab2(self):
        """Sets up the layout and widgets for Tab 2 (Magnon Dispersion)."""
        layout = QHBoxLayout(self.tab2)
        controls_layout = QVBoxLayout()
        vis_layout = QVBoxLayout()
        # Info Frame
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        title_label = QLabel("Magnon Dispersion (1D Chain)")
        title_label.setObjectName("titleLabel")
        desc_label = QLabel("<b>Spin waves (magnons)</b> are collective excitations. Energy ħω depends on wavevector <b>k</b> (related to wavelength λ). Relationship ħω(<b>k</b>) is <b>dispersion</b>.")
        desc_label.setWordWrap(True)
        desc_label.setObjectName("descLabel")
        desc_label2 = QLabel("For 1D chain (spacing 'a'), NN ferromagnetic J:")
        desc_label2.setWordWrap(True)
        desc_label2.setObjectName("descLabel")
        eq3_label = QLabel("ħω(k) = 2JS [ 1 - cos(ka) ] = 4JS sin²(ka/2)")
        eq3_label.setObjectName("eqLabel")
        eq3_label.setAlignment(Qt.AlignCenter)
        desc_label3 = QLabel("<b>Params:</b><br>• <b>J, S:</b> Energy scale.<br>• <b>a:</b> Sets Brillouin Zone (-π/a ≤ k ≤ +π/a).<br>• <b>k:</b> Selects wave (low k=long λ, high k=short λ).<br><i>Plot shows E vs k. Animation shows selected wave.</i>")
        desc_label3.setWordWrap(True)
        desc_label3.setObjectName("descLabel")
        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)
        info_layout.addWidget(desc_label2)
        info_layout.addWidget(eq3_label)
        info_layout.addWidget(desc_label3)
        info_layout.addStretch()
        # Visualization Area
        self.dispersion_plot_canvas = MplCanvas(self, width=5, height=3, dpi=100) # Real or placeholder
        vis_layout.addWidget(self.dispersion_plot_canvas)
        self.spin_chain_widget = SpinChainWidget()
        vis_layout.addWidget(self.spin_chain_widget)
        # Controls Frame
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_group_layout = QGridLayout(controls_frame)
        controls_group_layout.setSpacing(12)
        self.j2_label = QLabel()
        controls_group_layout.addWidget(self.j2_label, 0, 0, 1, 2)
        self.j2_slider = QSlider(Qt.Horizontal)
        self.j2_slider.setMinimum(1)
        self.j2_slider.setMaximum(200)
        self.j2_slider.setValue(100)
        self.j2_slider.valueChanged.connect(self.update_tab2_visuals)
        controls_group_layout.addWidget(self.j2_slider, 1, 0, 1, 2)
        self.s2_label = QLabel()
        controls_group_layout.addWidget(self.s2_label, 2, 0, 1, 2)
        self.s2_slider = QSlider(Qt.Horizontal)
        self.s2_slider.setMinimum(5)
        self.s2_slider.setMaximum(50)
        self.s2_slider.setValue(10)
        self.s2_slider.valueChanged.connect(self.update_tab2_visuals)
        controls_group_layout.addWidget(self.s2_slider, 3, 0, 1, 2)
        self.a2_label = QLabel()
        controls_group_layout.addWidget(self.a2_label, 4, 0, 1, 2)
        self.a2_slider = QSlider(Qt.Horizontal)
        self.a2_slider.setMinimum(50)
        self.a2_slider.setMaximum(200)
        self.a2_slider.setValue(100)
        self.a2_slider.valueChanged.connect(self.update_tab2_visuals)
        controls_group_layout.addWidget(self.a2_slider, 5, 0, 1, 2)
        self.k2_label = QLabel()
        controls_group_layout.addWidget(self.k2_label, 6, 0, 1, 2)
        self.k2_slider = QSlider(Qt.Horizontal)
        self.k2_slider.setMinimum(0)
        self.k2_slider.setMaximum(100)
        self.k2_slider.setValue(25)
        self.k2_slider.valueChanged.connect(self.update_tab2_visuals)
        controls_group_layout.addWidget(self.k2_slider, 7, 0, 1, 2)
        self.omega_info_label = QLabel()
        controls_group_layout.addWidget(self.omega_info_label, 8, 0, 1, 2)
        self.animate_chain_button = QPushButton("Start Wave")
        self.animate_chain_button.setToolTip("Start/Stop Wave Animation")
        self.animate_chain_button.setCheckable(True)
        self.animate_chain_button.toggled.connect(self.toggle_spin_chain_animation)
        controls_group_layout.addWidget(self.animate_chain_button, 9, 0, 1, 2)
        controls_group_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 10, 0)
        # Assemble Layouts
        controls_layout.addWidget(info_frame, 2)
        controls_layout.addWidget(controls_frame, 3)
        layout.addLayout(vis_layout, 7)
        layout.addLayout(controls_layout, 5)
        self.update_tab2_visuals() # Initial update

    def setup_tab3(self):
        """Sets up the layout and widgets for Tab 3 (Domain Wall)."""
        layout = QHBoxLayout(self.tab3)
        controls_layout = QVBoxLayout()
        vis_layout = QVBoxLayout()
        # Info Frame
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        title_label = QLabel("Continuum: Domain Wall Profile")
        title_label.setObjectName("titleLabel")
        desc_label = QLabel("Continuum (micromagnetics): <b>Exchange stiffness (A)</b> resists ∇<b>m</b>, <b>anisotropy (K)</b> favors easy axes.")
        desc_label.setWordWrap(True)
        desc_label.setObjectName("descLabel")
        eq4_label = QLabel("Exchange Energy Density ≈ A (∇<b>m</b>)²")
        eq4_label.setObjectName("eqLabel")
        eq4_label.setAlignment(Qt.AlignCenter)
        desc_label2 = QLabel("<b>Domain Wall</b>: Transition between domains, balances A & K. For 180° Bloch wall (uniaxial K):")
        desc_label2.setWordWrap(True)
        desc_label2.setObjectName("descLabel")
        eq_profile_label = QLabel("m<sub>z</sub>(x) = tanh(x/δ<sub>w</sub>),  m<sub>y</sub>(x) = sech(x/δ<sub>w</sub>)")
        eq_profile_label.setObjectName("eqLabel")
        eq_profile_label.setAlignment(Qt.AlignCenter)
        desc_label3 = QLabel("Characteristic <b>wall width (δ<sub>w</sub>)</b>:")
        desc_label3.setWordWrap(True)
        desc_label3.setObjectName("descLabel")
        eq_width_label = QLabel("δ<sub>w</sub> = π √(A / K)")
        eq_width_label.setObjectName("eqLabel")
        eq_width_label.setAlignment(Qt.AlignCenter)
        desc_label4 = QLabel("• Larger <b>A</b> → wider wall.<br>• Larger <b>K</b> → narrower wall.<br><i>Plot shows m<sub>y</sub>, m<sub>z</sub>. Animation shows spin rotation.</i>")
        desc_label4.setWordWrap(True)
        desc_label4.setObjectName("descLabel")
        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)
        info_layout.addWidget(eq4_label)
        info_layout.addWidget(desc_label2)
        info_layout.addWidget(eq_profile_label)
        info_layout.addWidget(desc_label3)
        info_layout.addWidget(eq_width_label)
        info_layout.addWidget(desc_label4)
        info_layout.addStretch()
        # Visualization Area
        self.dw_profile_canvas = MplCanvas(self, width=5, height=3, dpi=100) # Real or placeholder
        vis_layout.addWidget(self.dw_profile_canvas)
        self.domain_wall_widget = DomainWallWidget()
        vis_layout.addWidget(self.domain_wall_widget)
        # Controls Frame
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_group_layout = QGridLayout(controls_frame)
        controls_group_layout.setSpacing(12)
        self.a3_label = QLabel()
        controls_group_layout.addWidget(self.a3_label, 0, 0, 1, 2)
        self.a3_slider = QSlider(Qt.Horizontal)
        self.a3_slider.setMinimum(1)
        self.a3_slider.setMaximum(300)
        self.a3_slider.setValue(100)
        self.a3_slider.valueChanged.connect(self.update_tab3_visuals)
        controls_group_layout.addWidget(self.a3_slider, 1, 0, 1, 2)
        self.k3_label = QLabel()
        controls_group_layout.addWidget(self.k3_label, 2, 0, 1, 2)
        self.k3_slider = QSlider(Qt.Horizontal)
        self.k3_slider.setMinimum(1)
        self.k3_slider.setMaximum(500)
        self.k3_slider.setValue(100)
        self.k3_slider.valueChanged.connect(self.update_tab3_visuals)
        controls_group_layout.addWidget(self.k3_slider, 3, 0, 1, 2)
        self.delta_w_info_label = QLabel()
        self.delta_w_info_label.setStyleSheet("font-weight: bold; color: darkred;")
        controls_group_layout.addWidget(self.delta_w_info_label, 4, 0, 1, 2)
        controls_group_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0)
        # Assemble Layouts
        controls_layout.addWidget(info_frame, 2)
        controls_layout.addWidget(controls_frame, 1)
        layout.addLayout(vis_layout, 7)
        layout.addLayout(controls_layout, 5)
        self.update_tab3_visuals() # Initial update


    # --- Callback and Update Methods ---
    # (Methods remain unchanged from previous version)
    def on_j_slider_change(self, value):
        j_val = value / 100.0
        self.two_spin_widget.set_j(j_val)
        fm_radio = self.tab1.findChild(QRadioButton, "fm_radio")
        afm_radio = self.tab1.findChild(QRadioButton, "afm_radio")
        if fm_radio and afm_radio:
            fm_radio.blockSignals(True)
            afm_radio.blockSignals(True)
            if abs(j_val) < 1e-9: 
                fm_radio.setAutoExclusive(False)
                afm_radio.setAutoExclusive(False)
                fm_radio.setChecked(False)
                afm_radio.setChecked(False)
                fm_radio.setAutoExclusive(True)
                afm_radio.setAutoExclusive(True)
            elif j_val > 0: fm_radio.setChecked(True)
            else: afm_radio.setChecked(True)
            fm_radio.blockSignals(False)
            afm_radio.blockSignals(False)
            
    def set_j_sign(self, sign):
        current_j_abs = abs(self.two_spin_widget.J)
        new_j = sign * max(current_j_abs, 0.01)
        self.j_slider.blockSignals(True)
        self.j_slider.setValue(int(new_j * 100))
        self.j_slider.blockSignals(False)
        self.two_spin_widget.set_j(new_j)
        
    def on_s_slider_change(self, value):
        self.two_spin_widget.set_s(value / 10.0)
        
    def on_theta_slider_change(self, value):
        if not self.two_spin_widget.animating:
            self.two_spin_widget.set_s2_angle_deg(value)
            
    def update_tab1_labels(self):
        if not hasattr(self, 'j_label') or not self.j_label:
            return # Check if widget initialized
        j_val = self.two_spin_widget.J
        s_val = self.two_spin_widget.S
        theta_deg = np.degrees(self.two_spin_widget.s2_angle_rad)
        self.j_label.setText(f"J = {j_val:.2f} (Exchange Constant)")
        self.s_label.setText(f"S = {s_val:.1f} (Spin Magnitude)")
        if self.two_spin_widget.animating: 
            self.theta_label.setText(f"<i>Animating θ ≈ {theta_deg:.1f}°...</i>")
            self.theta_slider.setEnabled(False)
        else: 
            self.theta_label.setText(f"Manual θ = {theta_deg:.1f}°")
            self.theta_slider.setEnabled(True)
            self.theta_slider.blockSignals(True)
            self.theta_slider.setValue(int(theta_deg % 360))
            self.theta_slider.blockSignals(False)
            
    def update_energy_plot(self):
        if not MATPLOTLIB_AVAILABLE or not hasattr(self, 'energy_plot_canvas') or not self.energy_plot_canvas.axes:
            return # Check placeholder case
        ax = self.energy_plot_canvas.axes
        fig = self.energy_plot_canvas.figure
        theta_rad_current = self.two_spin_widget.s2_angle_rad
        J_current = self.two_spin_widget.J
        S_current = self.two_spin_widget.S
        theta_range_deg = np.linspace(0, 360, 200)
        theta_range_rad = np.radians(theta_range_deg)
        energy_range = -J_current * (S_current**2) * np.cos(theta_range_rad)
        if not np.all(np.isfinite(energy_range)) or abs(J_current) < 1e-9:
            energy_range = np.zeros_like(theta_range_rad)
        ax.clear()
        ax.plot(theta_range_deg, energy_range, label="E(θ) = -J S² cos(θ)", color='darkgreen', linewidth=2)
        current_energy = self.two_spin_widget.get_energy(theta_rad_current)
        ax.plot(np.degrees(theta_rad_current % (2*np.pi)), current_energy, 'ro', markersize=8, label='Current State')
        if J_current > 0: 
            ax.plot(0, -J_current * (S_current**2), 'm*', markersize=10, label='FM Ground State')
        elif J_current < 0: ax.plot(180, -J_current * (S_current**2), 'c*', markersize=10, label='AFM Ground State')
        ax.set_xlabel("Angle θ (degrees)")
        ax.set_ylabel("Energy (arb. units)")
        ax.set_title("Two-Spin Interaction Energy vs. Angle")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize='small', loc='upper right', bbox_to_anchor=(1.0, 1.15))
        ax.set_xlim(0, 360)
        if len(energy_range) > 0 and np.any(np.isfinite(energy_range)): 
            min_e, max_e = np.nanmin(energy_range), np.nanmax(energy_range)
            padding = (max_e - min_e) * 0.15 + 1e-6
            ax.set_ylim(min_e - padding, max_e + padding)
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        self.energy_plot_canvas.draw()
        
    def start_two_spin_animation(self, target_rad):
        self.theta_slider.setEnabled(False)
        self.two_spin_widget.start_animation(target_rad)
        
    def update_tab2_visuals(self):
        if not hasattr(self, 'j2_slider'):
            return # Check if widgets initialized
        J = self.j2_slider.value() / 100.0
        S = self.s2_slider.value() / 10
        a = self.a2_slider.value() / 100.0
        k_factor = self.k2_slider.value() / 100.0
        k_selected = k_factor * PI / a if a > 1e-6 else 0
        self.j2_label.setText(f"J = {J:.2f}")
        self.s2_label.setText(f"S = {S:.1f}")
        self.a2_label.setText(f"a = {a:.2f} (Lattice Spacing)")
        self.k2_label.setText(f"k = {k_factor:.2f} π/a")
        omega_max = 4 * J * S
        omega_selected = omega_max * (np.sin(k_selected * a / 2.0)**2) if a > 1e-6 else 0
        self.omega_info_label.setText(f"ħω(k) = {omega_selected:.3f} (Max: {omega_max:.3f})")
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'dispersion_plot_canvas') and self.dispersion_plot_canvas.axes:
            ax = self.dispersion_plot_canvas.axes
            fig = self.dispersion_plot_canvas.figure
            ax.clear()
            k_max = PI / a if a > 1e-6 else PI
            k_range = np.linspace(-k_max, k_max, 200)
            omega_range = omega_max * (np.sin(k_range * a / 2.0)**2) if a > 1e-6 else np.zeros_like(k_range)
            norm_factor = (PI/a if a > 1e-6 else 1.0) # Avoid division by zero if a is zero
            ax.plot(k_range / norm_factor, omega_range, label="ħω(k)", color='darkblue')
            ax.plot([k_selected / norm_factor], [omega_selected], 'ro', markersize=8, label='Selected k')
            ax.set_xlabel("k / (π/a)")
            ax.set_ylabel("Energy ħω (arb. units)")
            ax.set_title("1D Magnon Dispersion Relation")
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_ylim(-0.05 * max(omega_max, 1e-9), max(omega_max * 1.1, 0.1)) # Ensure non-zero range
            ax.set_xlim(-1.05, 1.05)
            ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%g $\\pi/a$'))
            ax.xaxis.set_major_locator(mticker.MultipleLocator(base=0.5))
            ax.legend(fontsize='small')
            fig.tight_layout()
            self.dispersion_plot_canvas.draw()
        if hasattr(self, 'spin_chain_widget'):
            visual_a = self.spin_chain_widget.a_pixels
            k_visual = k_factor * PI / visual_a if visual_a > 1e-6 else 0
            self.spin_chain_widget.set_params(k=k_visual, omega=omega_selected, a_pixels=visual_a)
            
    def toggle_spin_chain_animation(self, checked):
         if hasattr(self, 'spin_chain_widget'):
            self.animate_chain_button.setText("Stop Wave" if checked else "Start Wave")
            if checked: 
                self.spin_chain_widget.start_animation()
            else:
                self.spin_chain_widget.stop_animation()
                
    def update_tab3_visuals(self):
        # (Keep the initial part calculating A_val, K_val, delta_w, and updating labels)
        if not hasattr(self, 'a3_slider'): return # Check if widgets initialized

        # Get values from sliders
        A_val = self.a3_slider.value() / 10.0 * 1e-12; K_val = self.k3_slider.value() * 1e3
        self.a3_label.setText(f"A = {A_val*1e12:.1f} pJ/m (Stiffness)")
        self.k3_label.setText(f"K = {K_val*1e-3:.0f} kJ/m³ (Anisotropy)")

        # Calculate physical wall width delta_w = pi * sqrt(A / K)
        delta_w = 0.0
        if K_val > 1e-9: # Avoid division by zero / negative K issues
            delta_w = PI * np.sqrt(A_val / K_val) if A_val >= 0 else -1.0
        else:
            delta_w = float('inf') # Infinite width if K=0

        # Update label (convert meters to nm)
        if delta_w == float('inf'): self.delta_w_info_label.setText("<b>Wall Width δ<sub>w</sub> = ∞ (K≈0)</b>")
        elif delta_w < 0: self.delta_w_info_label.setText("<b>Wall Width δ<sub>w</sub> (Invalid A<0)</b>")
        else: self.delta_w_info_label.setText(f"<b>Wall Width δ<sub>w</sub> = {delta_w * 1e9:.2f} nm</b>")

        # Update Domain Wall Profile Plot
        # (Keep the Matplotlib plotting section as before)
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'dw_profile_canvas') and self.dw_profile_canvas.axes:
            # ... (plotting code remains the same) ...
            ax = self.dw_profile_canvas.axes; fig = self.dw_profile_canvas.figure; ax.clear()
            if delta_w > 0 and delta_w != float('inf'):
                x_range_val = self.domain_wall_widget.x_range_factor * delta_w; x_plot = np.linspace(-x_range_val, x_range_val, 300)
                x_norm = x_plot / delta_w if delta_w > 1e-18 else x_plot * 1e18 # Avoid division by tiny delta_w
                mz_profile = np.tanh(x_norm); my_profile = 1.0 / np.cosh(x_norm)
                ax.plot(x_plot * 1e9, mz_profile, label='m$_z$(x) = tanh(x/δ$_w$)', color='darkblue')
                ax.plot(x_plot * 1e9, my_profile, label='m$_y$(x) = sech(x/δ$_w$)', color='darkred', linestyle='--')
                label_dw = f'±δ$_w$ ({delta_w*1e9:.1f} nm)' if delta_w*1e9 < 1000 else f'±δ$_w$ ({delta_w*1e6:.1f} µm)'
                ax.axvline(delta_w * 1e9, color='gray', linestyle=':', label=label_dw); ax.axvline(-delta_w * 1e9, color='gray', linestyle=':')
                ax.set_xlabel("Position x (nm)")
            else:
                 ax.axhline(1, color='darkblue', linestyle='--', label='m$_z$ (Uniform)'); ax.axhline(0, color='darkred', linestyle='--', label='m$_y$ (Uniform)'); ax.set_xlabel("Position x")
            ax.set_ylabel("Magnetization Component"); ax.set_title("Bloch Domain Wall Profile (180°)"); ax.grid(True, linestyle='--', alpha=0.6); ax.set_ylim(-1.1, 1.1); ax.legend(fontsize='small'); fig.tight_layout(); self.dw_profile_canvas.draw()


        # --- Update Domain Wall Widget ---
        if hasattr(self, 'domain_wall_widget'):
            # **** CORRECTED SCALING LOGIC ****
            # Use a fixed scaling factor to map physical nm to visual pixels.
            # Adjust this factor to control the visual size variation.
            pixels_per_nm = 5.0
            delta_w_pixels = 1.0 # Default visual width for invalid cases (A<0)

            if delta_w > 0 and delta_w != float('inf'):
                # Calculate visual width directly from physical width (in nm) and scaling factor
                delta_w_pixels = delta_w * 1e9 * pixels_per_nm
            elif K_val < 1e-9: # K is zero or negative -> infinite physical width
                # Make the visual width very large to represent this
                delta_w_pixels = self.domain_wall_widget.width() * 5 # e.g., 5 times widget width

            # Ensure minimum visual width (using the constant defined earlier)
            min_visual_width = GRID_SPACING / 5.0
            delta_w_pixels = max(delta_w_pixels, min_visual_width)

            # Pass the calculated *visual* width to the widget
            self.domain_wall_widget.set_delta_w(delta_w_pixels)
            # **********************************

    # --- Common Methods ---
    def setup_spin_widget_update_signal(self, widget):
        """Patches the widget's update() method to also emit a signal."""
        if hasattr(widget, 'update') and not hasattr(widget, '_original_update'):
            widget._original_update = widget.update
            def new_update(*args, **kwargs):
                widget._original_update(*args, **kwargs)
                if hasattr(widget, 'update_signal') and widget.update_signal: widget.update_signal.updated.emit()
            widget.update = new_update
    def closeEvent(self, event):
        """Ensures timers are stopped when the window is closed."""
        print("Closing application and stopping timers...")
        if hasattr(self, 'two_spin_widget'): self.two_spin_widget.stop_animation()
        if hasattr(self, 'spin_chain_widget'): self.spin_chain_widget.stop_animation()
        event.accept()

# =============================================================================
# Main Execution Block
# =============================================================================
if __name__ == '__main__':
    # --- Set High DPI Attributes BEFORE Creating QApplication ---
    # This MUST happen before 'app = QApplication(sys.argv)'
    print("Setting High DPI Scaling Attributes...")
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        print("  - AA_EnableHighDpiScaling set.")
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        print("  - AA_UseHighDpiPixmaps set.")

    # --- Create QApplication Instance ---
    print("Creating QApplication...")
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    print("QApplication created.")

    # --- Create Main Window ---
    print("Creating ExchangeAnimator window...")
    window = ExchangeAnimator()
    print("ExchangeAnimator window created.")

    # --- Patch Update Method (requires window instance) ---
    if hasattr(window, 'two_spin_widget'):
        print("Patching update method for TwoSpinWidget...")
        window.setup_spin_widget_update_signal(window.two_spin_widget)

    # --- Show Window ---
    print("Showing window...")
    window.show()

    # --- Start Event Loop ---
    print("Starting application event loop...")
    sys.exit(app.exec_())
