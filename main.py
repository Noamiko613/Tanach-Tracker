import sys
import json
import os
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QPushButton, QScrollArea, QMessageBox, QGraphicsOpacityEffect
)
# CORRECTED IMPORT: Added QPointF for use in QPainterPath
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QRect, pyqtProperty, QPointF 
from PyQt6.QtGui import QIcon, QPainter, QColor, QPen, QFont, QPainterPath

# DEBUG MODE - Set to True to enable testing features, False for production
DEBUG = False

def num_to_hebrew(num):
    hebrew_nums = [
        "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "יא", "יב", "יג", "יד", "טו",
        "טז", "יז", "יח", "יט", "כ", "כא", "כב", "כג", "כד", "כה", "כו", "כז", "כח", "כט", "ל",
        "לא", "לב", "לג", "לד", "לה", "לו", "לז", "לח", "לט", "מ", "מא", "מב", "מג", "מד", "מה",
        "מו", "מז", "מח", "מט", "נ", "נא", "נב", "נג", "נד", "נה", "נו", "נז", "נח", "נט", "ס",
        "סא", "סב", "סג", "סד", "סה", "סו", "סז", "סח", "סט", "ע", "עא", "עב", "עג", "עד", "עה",
        "עו", "עז", "עח", "עט", "פ", "פא", "פב", "פג", "פד", "פה", "פו", "פז", "פח", "פט", "צ",
        "צא", "צב", "צג", "צד", "צה", "צו", "צז", "צח", "צט", "ק", "קא", "קב", "קג", "קד", "קה",
        "קו", "קז", "קח", "קט", "קי", "קיא", "קיב", "קיג", "קיד", "קטו", "קטז", "קיז", "קיח", "קיט",
        "קכ", "קכא", "קכב", "קכג", "קכד", "קכה", "קכו", "קכז", "קכח", "קכט", "קל", "קלא", "קלב", "קלג",
        "קלד", "קלה", "קלו", "קלז", "קלח", "קלט", "קמ", "קמא", "קמב", "קמג", "קמד", "קמה", "קמו",
        "קמז", "קמח", "קמט", "קנ"
    ]
    return hebrew_nums[num - 1] if 1 <= num <= 150 else str(num)

BOOKS = {
    "תורה": [("בראשית", 50), ("שמות", 40), ("ויקרא", 27), ("במדבר", 36), ("דברים", 34)],
    "נביאים": [
        ("יהושע", 24), ("שופטים", 21), ("שמואל א", 31), ("שמואל ב", 24), ("מלכים א", 22),
        ("מלכים ב", 25), ("ישעיהו", 66), ("ירמיהו", 52), ("יחזקאל", 48), ("הושע", 14),
        ("יואל", 4), ("עמוס", 9), ("עובדיה", 1), ("יונה", 4), ("מיכה", 7), ("נחום", 3),
        ("חבקוק", 3), ("צפניה", 3), ("חגי", 2), ("זכריה", 14), ("מלאכי", 4)
    ],
    "כתובים (ללא תהילים)": [
        ("משלי", 31), ("איוב", 42), ("שיר השירים", 8), ("רות", 4), ("איכה", 5), ("קהלת", 12),
        ("אסתר", 10), ("דניאל", 12), ("עזרא", 10), ("נחמיה", 13), ("דברי הימים א", 29),
        ("דברי הימים ב", 36)
    ],
    "תהילים": [("תהילים", 150)]
}

def generate_plans(duration):
    plans = {}
    for category, books in BOOKS.items():
        total = sum(c for _, c in books)
        per_day = total / duration
        book_idx, chapter = 0, 1
        for day in range(1, duration + 1):
            # Use floating point for precision, then round the difference
            needed = round(day * per_day) - round((day - 1) * per_day)
            daily = []
            while needed > 0 and book_idx < len(books):
                book, max_chap = books[book_idx]
                left = max_chap - chapter + 1
                if needed >= left:
                    daily.append(f"{book}: פרק {num_to_hebrew(chapter)} - פרק {num_to_hebrew(max_chap)}")
                    book_idx += 1
                    chapter = 1
                    needed -= left
                else:
                    end = chapter + needed - 1
                    daily.append(f"{book}: פרק {num_to_hebrew(chapter)} - פרק {num_to_hebrew(end)}")
                    chapter = end + 1
                    needed = 0
            plans.setdefault(day, {})[category] = ", ".join(daily)
    return plans

PLANS = {
    "30 יום": generate_plans(30),
    "60 יום": generate_plans(60),
    "90 יום": generate_plans(90)
}

def save_progress(progress):
    with open("progress.json", "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=4)

def load_progress():
    try:
        with open("progress.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_output_path(filename):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

class AnimatedCheckBox(QCheckBox):
    def __init__(self, text):
        super().__init__(text)
        self._scale = 1.0
        self.original_style = ""
        self.stateChanged.connect(self.animate_check)

    def animate_check(self):
        # Enhanced scale pulse animation
        self.anim = QPropertyAnimation(self, b"scale")
        self.anim.setDuration(400)
        self.anim.setStartValue(1.0)
        self.anim.setKeyValueAt(0.3, 1.2)
        self.anim.setKeyValueAt(0.6, 0.95)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutElastic)
        self.anim.start()
        
        # Color pulse effect
        if self.isChecked():
            self.setStyleSheet("""
                QCheckBox { color: #2ecc71; font-weight: bold; }
                QCheckBox::indicator:checked { background-color: #2ecc71; border: 2px solid #27ae60; }
            """)
        else:
            self.setStyleSheet("")
            
        # Opacity flash effect
        effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(effect)
        self.opacity_anim = QPropertyAnimation(effect, b"opacity")
        self.opacity_anim.setDuration(400)
        self.opacity_anim.setStartValue(0.3)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.opacity_anim.finished.connect(lambda: self.setGraphicsEffect(None))
        self.opacity_anim.start()

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update() # Force repaint to apply transform (might need custom paint logic for true scale)

class ConfettiWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.confetti_pieces = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_confetti)

    def start_confetti(self, duration=3000, intensity=1.0):
        self.confetti_pieces = []
        colors = [
            QColor(255, 100, 100), QColor(100, 255, 100), QColor(100, 100, 255),
            QColor(255, 255, 100), QColor(255, 100, 255), QColor(100, 255, 255),
            QColor(255, 150, 50), QColor(150, 50, 255), QColor(50, 255, 150)
        ]
        particle_count = int(80 * intensity)
        for _ in range(particle_count):
            self.confetti_pieces.append({
                'x': random.randint(0, self.width()), 'y': random.randint(-100, -20),
                'vx': random.uniform(-3, 3), 'vy': random.uniform(3, 7),
                'color': random.choice(colors), 'size': random.randint(6, 15),
                'rotation': random.uniform(0, 360), 'rotation_speed': random.uniform(-10, 10),
                'shape': random.choice(['circle', 'rect', 'star'])
            })
        self.timer.start(30)
        QTimer.singleShot(duration, self.stop_confetti)
        self.raise_()
        self.show()

    def stop_confetti(self):
        self.timer.stop()
        self.confetti_pieces = []
        self.hide()

    def update_confetti(self):
        for piece in self.confetti_pieces:
            piece['x'] += piece['vx']
            piece['y'] += piece['vy']
            piece['vy'] += 0.3  # gravity
            piece['rotation'] += piece['rotation_speed']
            piece['vx'] *= 0.99  # air resistance
        self.confetti_pieces = [p for p in self.confetti_pieces if p['y'] < self.height() + 20]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for piece in self.confetti_pieces:
            painter.save()
            painter.translate(piece['x'], piece['y'])
            painter.rotate(piece['rotation'])
            painter.setBrush(piece['color'])
            painter.setPen(Qt.PenStyle.NoPen)
            size = piece['size']
            half = size // 2
            if piece['shape'] == 'circle':
                painter.drawEllipse(-half, -half, size, size)
            elif piece['shape'] == 'rect':
                painter.drawRect(-half, -half, size, size)
            else:  # star
                # Use QPointF here for safety in polygon drawing
                painter.drawPolygon([
                    QPointF(0, -half), QPointF(half//3, -half//4), QPointF(half, 0),
                    QPointF(half//3, half//4), QPointF(0, half), QPointF(-half//3, half//4),
                    QPointF(-half, 0), QPointF(-half//3, -half//4)
                ])
            painter.restore()

class TrophyShelf(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.trophies = []
        self.animating_trophy = None
        self.total_trophy_count = 0
        self.max_visible_trophies = 8

    def set_trophy_count(self, count):
        self.total_trophy_count = count
        # Only show up to max_visible_trophies on shelf
        visible_count = min(count, self.max_visible_trophies)
        self.trophies = [{'x': 50 + i * 50, 'y': 30, 'scale': 1.0} for i in range(visible_count)]
        self.update()

    def add_trophy_animated(self):
        """Add a new trophy with animation"""
        self.total_trophy_count += 1
        # Only animate if we haven't reached max visible trophies
        if len(self.trophies) < self.max_visible_trophies:
            new_x = 50 + len(self.trophies) * 50
            self.animating_trophy = {
                'x': new_x, 'y': -50,  # Start above
                'scale': 0.5, 'opacity': 0.0
            }
            # Animate the trophy dropping in
            self.animation_timer = QTimer()
            self.animation_frame = 0
            self.animation_timer.timeout.connect(self.animate_trophy_frame)
            self.animation_timer.start(30)
            self.raise_()
            self.show()
        else:
            # Just update the counter, no animation
            self.update()

    def animate_trophy_frame(self):
        if self.animating_trophy is None:
            self.animation_timer.stop()
            return
            
        self.animation_frame += 1
        progress = min(self.animation_frame / 30.0, 1.0)  # 30 frames = ~1 second
        
        # Bounce easing
        if progress < 1.0:
            self.animating_trophy['y'] = -50 + (80 * progress)
            self.animating_trophy['scale'] = 0.5 + (0.5 * progress)
            self.animating_trophy['opacity'] = progress
        else:
            # Animation complete - add to permanent trophies
            self.trophies.append({
                'x': self.animating_trophy['x'], 'y': 30, 'scale': 1.0
            })
            self.animating_trophy = None
            self.animation_timer.stop()
            # Small bounce on landing if self.trophies:
            self.bounce_trophy(len(self.trophies) - 1)
            
        self.update()

    def bounce_trophy(self, index):
        """Make a trophy bounce when it lands"""
        # Simple bounce effect - could be enhanced
        pass

    def paintEvent(self, event):
        # Check if widget is properly initialized
        if not self.isVisible() or self.width() == 0 or self.height() == 0:
            return
            
        painter = QPainter(self)
        if not painter.isActive():
            return
            
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw trophy counter if we have more than max visible
        if self.total_trophy_count > 0:
            painter.setPen(QColor(218, 165, 32))
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            painter.setFont(font)
            counter_text = f"🏆 × {self.total_trophy_count}"
            painter.drawText(self.width() - 100, 15, counter_text)
            
        # Draw shelf background with 3D effect
        # Darker bottom edge
        painter.setBrush(QColor(101, 67, 33))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(10, 60, self.width() - 20, 15, 5, 5)
        # Main shelf surface
        painter.setBrush(QColor(139, 69, 19))
        painter.drawRoundedRect(10, 55, self.width() - 20, 15, 5, 5)
        # Shelf highlight
        painter.setBrush(QColor(160, 82, 45, 150))
        painter.drawRoundedRect(12, 56, self.width() - 24, 5, 3, 3)

        # Draw permanent trophies
        for trophy in self.trophies:
            self.draw_trophy(painter, trophy['x'], trophy['y'], trophy['scale'], 1.0)
            
        # Draw animating trophy
        if self.animating_trophy:
            self.draw_trophy(
                painter, self.animating_trophy['x'], self.animating_trophy['y'],
                self.animating_trophy['scale'], self.animating_trophy['opacity']
            )
            
        painter.end()

    def draw_trophy(self, painter, x, y, scale, opacity):
        """Draws a more realistic, professional-looking trophy."""
        # Gold colors for realism
        GOLD_DARK = QColor(139, 101, 8)    # Deep shadow gold
        GOLD_BASE = QColor(218, 165, 32)   # Base gold color
        GOLD_LIGHT = QColor(255, 223, 0)   # Highlight gold
        GOLD_SHINE = QColor(255, 250, 205, 180) # White shine

        painter.save()
        painter.setOpacity(opacity)
        painter.translate(x, y)
        painter.scale(scale, scale)
        
        # 1. Draw Shadow
        painter.setBrush(QColor(0, 0, 0, 60))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-12, 28, 24, 4)
        
        # 2. Draw Base Platform (Layered 3D)
        # Wide base layer 1 (Dark)
        painter.setBrush(GOLD_DARK)
        painter.drawRect(-14, 25, 28, 4)
        # Wide base layer 2 (Base)
        painter.setBrush(GOLD_BASE)
        painter.drawRect(-13, 25, 26, 3)
        # Base platform
        painter.drawRect(-8, 22, 16, 3)
        
        # 3. Draw Stem (Tapered)
        # FIX: Use QPointF to start QPainterPath
        stem_path = QPainterPath(QPointF(-4, 22))
        stem_path.lineTo(QPointF(-3, 17))
        stem_path.lineTo(QPointF(3, 17))
        stem_path.lineTo(QPointF(4, 22))
        painter.fillPath(stem_path, GOLD_DARK)
        
        # 4. Draw Cup Body (Curved and Tapered)
        # Back half/Shadow
        # FIX: Use QPointF
        cup_path_back = QPainterPath(QPointF(-12, -7))
        cup_path_back.cubicTo(QPointF(-18, 5), QPointF(-15, 17), QPointF(-8, 20))
        cup_path_back.lineTo(QPointF(8, 20))
        cup_path_back.cubicTo(QPointF(15, 17), QPointF(18, 5), QPointF(12, -7))
        painter.setBrush(GOLD_DARK)
        painter.setPen(QPen(GOLD_DARK, 1))
        painter.drawPath(cup_path_back)

        # Front half/Main gold
        # FIX: Use QPointF
        cup_path_front = QPainterPath(QPointF(-10, -5))
        cup_path_front.cubicTo(QPointF(-15, 5), QPointF(-12, 16), QPointF(-6, 19))
        cup_path_front.lineTo(QPointF(6, 19))
        cup_path_front.cubicTo(QPointF(12, 16), QPointF(15, 5), QPointF(10, -5))
        painter.setBrush(GOLD_BASE)
        painter.setPen(QPen(GOLD_BASE, 2))
        painter.drawPath(cup_path_front)
        
        # 5. Draw Rim and Inner Shadow
        # Top rim (light gold)
        painter.setBrush(GOLD_LIGHT)
        painter.setPen(QPen(GOLD_BASE, 1))
        painter.drawEllipse(-12, -9, 24, 6)
        # Inner rim shadow (depth)
        painter.setBrush(GOLD_DARK.darker(150))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-10, -8, 20, 4)

        # 6. Draw Handles (Curved and clean)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(GOLD_BASE, 2, cap=Qt.PenCapStyle.RoundCap))
        
        # Left Handle
        # FIX: Use QPointF
        handle_left = QPainterPath(QPointF(-10, 0))
        handle_left.quadTo(QPointF(-25, -10), QPointF(-18, 12))
        painter.drawPath(handle_left)
        
        # Right Handle
        # FIX: Use QPointF
        handle_right = QPainterPath(QPointF(10, 0))
        handle_right.quadTo(QPointF(25, -10), QPointF(18, 12))
        painter.drawPath(handle_right)

        # 7. Draw Gem/Crest (Professional Top Element)
        painter.setBrush(QColor(0, 102, 204)) # Sapphire Blue
        painter.setPen(QPen(QColor(0, 51, 102), 1))
        
        # Shield/Gem Shape
        # FIX: Use QPointF
        crest_points = [
            QPointF(0, -20), QPointF(5, -15), QPointF(5, -8), QPointF(0, -5),
            QPointF(-5, -8), QPointF(-5, -15)
        ]
        painter.drawPolygon(crest_points)
        
        # Gem reflection/shine
        painter.setBrush(QColor(173, 216, 230, 180)) # Light Blue
        painter.drawEllipse(-1, -17, 2, 4)

        # 8. Draw Main Vertical Highlight (Final Touch)
        painter.setBrush(GOLD_SHINE)
        # FIX: Use QPointF
        highlight_path = QPainterPath(QPointF(-6, -3))
        highlight_path.lineTo(QPointF(-3, 15))
        highlight_path.lineTo(QPointF(-1, 15))
        highlight_path.lineTo(QPointF(-4, -3))
        painter.fillPath(highlight_path, GOLD_SHINE)

        painter.restore()

class CelebrationLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                font-size: 26px; font-weight: bold; color: #1b5e20; padding: 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(129, 199, 132, 0.9), stop:1 rgba(102, 187, 106, 0.9));
                border-radius: 15px; border: 3px solid #4caf50;
            }
        """)

    def animate_in(self):
        # Fade and scale in animation
        effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(effect)
        self.fade = QPropertyAnimation(effect, b"opacity")
        self.fade.setDuration(800)
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade.finished.connect(lambda: self.setGraphicsEffect(None))
        self.fade.start()
        
        # Bounce effect
        self.geometry_anim = QPropertyAnimation(self, b"geometry")
        self.geometry_anim.setDuration(800)
        start_rect = self.geometry()
        center = start_rect.center()
        # Start from a tiny rectangle centered on the final position
        small_rect = QRect(center.x(), center.y(), 0, 0) 
        self.geometry_anim.setStartValue(small_rect)
        self.geometry_anim.setEndValue(start_rect)
        self.geometry_anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.geometry_anim.start()

class TanachTracker(QWidget):
    def __init__(self):
        super().__init__()
        # NOTE: Ensure 'torah_icon.ico' exists or remove this line for error-free startup
        try:
            # Fallback icon if the file doesn't exist
            if os.path.exists("torah_icon.ico"):
                 self.setWindowIcon(QIcon("torah_icon.ico"))
        except Exception:
            pass 
            
        self.setWindowTitle("מעקב לימוד תנ\"ך")
        self.resize(600, 600)
        self.progress = load_progress()
        self.plan = self.progress.get("plan", "30 יום")
        self.day = self.progress.get(self.plan + "_day", 1)
        self.checkboxes = {}
        self.celebration_label = None
        self.confetti = None
        self.last_message = None  # Track last motivational message
        self.trophy_shelf = None
        self.save_effect = None # FIX: Holder for the QGraphicsOpacityEffect

        self.setup_ui()
        
        # Setup confetti overlay
        self.confetti = ConfettiWidget(self)
        self.confetti.setGeometry(self.rect())
        self.confetti.hide()
        
        # Setup trophy shelf
        self.trophy_shelf = TrophyShelf(self)
        self.trophy_shelf.setGeometry(0, 0, self.width(), 80)
        completion_count = self.progress.get("completion_count", 0)
        self.trophy_shelf.set_trophy_count(completion_count)
        
        self.update_checklist()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Add spacing for trophy shelf at top
        self.layout.addSpacing(85)
        
        self.plan_label = QLabel("בחר תוכנית:")
        self.plan_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.layout.addWidget(self.plan_label)
        
        self.plan_selector = QComboBox()
        self.plan_selector.addItems(PLANS.keys())
        self.plan_selector.setCurrentText(self.plan)
        self.plan_selector.currentTextChanged.connect(self.change_plan)
        self.layout.addWidget(self.plan_selector)
        
        self.day_label = QLabel("")
        self.layout.addWidget(self.day_label)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.checklist_widget = QWidget()
        self.checklist_layout = QVBoxLayout()
        self.checklist_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.checklist_widget.setLayout(self.checklist_layout)
        self.scroll_area.setWidget(self.checklist_widget)
        self.layout.addWidget(self.scroll_area)
        
        self.save_button = QPushButton("שמור התקדמות")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)

        # DEBUG: Jump to last day button for testing
        if DEBUG:
            self.jump_button = QPushButton("🔧 DEBUG: קפוץ ליום האחרון")
            self.jump_button.clicked.connect(self.jump_to_last_day)
            self.jump_button.setStyleSheet("""
                QPushButton { background-color: #ff9800; color: white; font-weight: bold; padding: 8px; border-radius: 5px; }
                QPushButton:hover { background-color: #f57c00; }
            """)
            self.layout.addWidget(self.jump_button)
            
        self.save_status = QLabel("")
        self.layout.addWidget(self.save_status)
        
        self.restart_button = QPushButton("התחל מחדש את התוכנית")
        self.restart_button.clicked.connect(self.restart_plan)
        self.restart_button.hide()
        self.layout.addWidget(self.restart_button)

    def change_plan(self, new_plan):
        self.plan = new_plan
        self.day = self.progress.get(self.plan + "_day", 1)
        self.progress["plan"] = self.plan
        self.update_checklist()

    def update_checklist(self):
        # Clear old widgets
        for i in reversed(range(self.checklist_layout.count())):
            widget = self.checklist_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        self.day_label.setText(f"יום מספר: {self.day}")
        today = PLANS[self.plan].get(self.day, {})
        self.checkboxes = {}
        
        for category, text in today.items():
            checkbox = AnimatedCheckBox(f"{category}: {text}")
            checkbox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            # Check progress from stored data
            checkbox.setChecked(
                self.progress.get(self.plan, {}).get(str(self.day), {}).get(category, False)
            )
            checkbox.stateChanged.connect(lambda _, cat=category: self.toggle(cat))
            self.checkboxes[category] = checkbox
            self.checklist_layout.addWidget(checkbox)
            
        self.write_progress_txt()
        
        if self.day > len(PLANS[self.plan]):
            self.show_completion_message()
        else:
            # Show checklist items again if they were hidden by completion message
            for i in range(self.checklist_layout.count()):
                widget = self.checklist_layout.itemAt(i).widget()
                if widget:
                    widget.show()
            self.save_button.show()
            self.save_status.show()
            self.plan_selector.setEnabled(True)
            self.restart_button.hide()

    def toggle(self, category):
        day_data = self.progress.setdefault(self.plan, {}).setdefault(str(self.day), {})
        day_data[category] = self.checkboxes[category].isChecked()

    def save(self):
        self.progress["plan"] = self.plan
        self.progress[self.plan + "_day"] = self.day
        
        all_checked = all(cb.isChecked() for cb in self.checkboxes.values())
        total_days = len(PLANS[self.plan])
        is_last_day = (self.day == total_days)

        if all_checked and self.checkboxes:
            if not is_last_day:
                self.show_day_completion_animation()
                self.day += 1
                self.progress[self.plan + "_day"] = self.day
                
                # Check for milestones
                if self.day == total_days // 2 + 1:  # Halfway
                    QTimer.singleShot(800, self.show_halfway_celebration)
                elif self.day == (total_days * 3) // 4 + 1:  # 75% done
                    QTimer.singleShot(800, self.show_three_quarter_celebration)
                    
                QTimer.singleShot(1500, self.update_checklist)
            else:
                # Last day - completion handled in update_checklist on next call
                self.day += 1 
                self.progress[self.plan + "_day"] = self.day
                self.update_checklist()
        else:
            # Not all checked, just save current progress
            self.update_checklist()
            
        save_progress(self.progress)
        self.write_progress_txt()
        self.animate_save_status()

    def write_progress_txt(self):
        with open(get_output_path("progress.txt"), "w", encoding="utf-8") as f:
            f.write("מעקב לימוד תנ\"ך\n\n")
            f.write(f"תוכנית נבחרת: {self.plan}\n")
            f.write(f"יום נוכחי: {self.day}\n\n")
            f.write("משימות ליום זה:\n")
            today = PLANS[self.plan].get(self.day, {})
            for cat, txt in today.items():
                done = self.progress.get(self.plan, {}).get(str(self.day), {}).get(cat, False)
                mark = "✔️ הושלם" if done else "❌ לא הושלם"
                f.write(f"{cat}: {txt} - {mark}\n")
            f.write("\nהמשימות שעדיין לא הושלמו יוצגו ביום הבא.\n")

    def animate_save_status(self):
        self.save_status.setText("✔️ התקדמות נשמרה בהצלחה!")
        
        # FIX: Attach effect to self to prevent it from being garbage collected
        self.save_effect = QGraphicsOpacityEffect() 
        self.save_status.setGraphicsEffect(self.save_effect)
        
        fade_in = QPropertyAnimation(self.save_effect, b"opacity")
        fade_in.setDuration(400)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.start()
        
        # Pass no arguments to lambda since effect is now a persistent attribute
        QTimer.singleShot(2000, self.fade_out_status) 

    def fade_out_status(self):
        # FIX: Check if effect is still valid before use
        if self.save_effect is None:
            return

        fade_out = QPropertyAnimation(self.save_effect, b"opacity")
        fade_out.setDuration(400)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        
        def cleanup():
            self.save_status.setText("")
            # Important: Delete the effect after animation is complete
            self.save_status.setGraphicsEffect(None)
            self.save_effect = None 
            
        fade_out.finished.connect(cleanup)
        fade_out.start()

    def show_day_completion_animation(self):
        # Enhanced confetti burst
        if self.confetti:
            self.confetti.start_confetti(duration=2500, intensity=1.2)
            
        # Show temporary celebration message
        if self.celebration_label:
            self.layout.removeWidget(self.celebration_label)
            self.celebration_label.deleteLater()
            
        messages = [
            "🎉 יפה מאוד! יום נוסף הושלם!", "💪 כל הכבוד! ממשיכים קדימה!",
            "⭐ מצוין! עוד יום של התקדמות!", "🌟 נהדר! הולכים חזק!",
            "🔥 מעולה! עוד יום מוצלח!", "✨ כל הכבוד! התקדמות מרשימה!"
        ]
        
        # Avoid repeating the same message
        available_messages = [msg for msg in messages if msg != self.last_message]
        chosen_message = random.choice(available_messages)
        self.last_message = chosen_message
        
        self.celebration_label = CelebrationLabel(chosen_message)
        self.layout.insertWidget(2, self.celebration_label) # Insert above Save button
        self.celebration_label.animate_in()
        
        QTimer.singleShot(3000, self.remove_celebration_label)

    def show_halfway_celebration(self):
        if self.confetti:
            self.confetti.start_confetti(duration=5000, intensity=1.5)
            
        msg = QMessageBox(self)
        msg.setWindowTitle("🎊 יישר כוח! 🎊")
        msg.setText(
            "🎉 מדהים! הגעת לחצי מהתוכנית! 🎉\n\n"
            "אתה עושה עבודה מצוינת!\n"
            "כבר סיימת 50% מהדרך!\n\n"
            "המשך בעבודה הטובה! 💪"
        )
        
        # Scale font and dimensions based on window size
        scale_factor = min(self.width() / 600, self.height() / 600)
        font_size = int(18 * scale_factor)
        min_width = int(300 * scale_factor)
        padding = int(20 * scale_factor)
        button_padding = f"{int(10 * scale_factor)}px {int(30 * scale_factor)}px"
        
        msg.setStyleSheet(f"""
            QMessageBox {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fff8e1, stop:1 #ffe082); border: 3px solid #ffa726; border-radius: 15px; }}
            QMessageBox QLabel {{ font-size: {font_size}px; font-weight: bold; color: #e65100; padding: {padding}px; min-width: {min_width}px; }}
            QPushButton {{ background-color: #ffa726; color: white; font-size: {int(14 * scale_factor)}px; font-weight: bold; padding: {button_padding}; border-radius: 8px; border: none; }}
            QPushButton:hover {{ background-color: #ff9800; }}
        """)
        msg.exec()

    def show_three_quarter_celebration(self):
        if self.confetti:
            self.confetti.start_confetti(duration=4500, intensity=1.4)
            
        msg = QMessageBox(self)
        msg.setWindowTitle("🚀 כמעט בסיום! 🚀")
        msg.setText(
            "💫 אתה ב-75% מהדרך! 💫\n\n"
            "התקדמות מרשימה!\n"
            "רק עוד רבע מהדרך!\n\n"
            "הסיום ממש קרוב! 🎯"
        )
        
        # Scale font and dimensions based on window size
        scale_factor = min(self.width() / 600, self.height() / 600)
        font_size = int(18 * scale_factor)
        min_width = int(300 * scale_factor)
        padding = int(20 * scale_factor)
        button_padding = f"{int(10 * scale_factor)}px {int(30 * scale_factor)}px"
        
        msg.setStyleSheet(f"""
            QMessageBox {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e3f2fd, stop:1 #90caf9); border: 3px solid #42a5f5; border-radius: 15px; }}
            QMessageBox QLabel {{ font-size: {font_size}px; font-weight: bold; color: #0d47a1; padding: {padding}px; min-width: {min_width}px; }}
            QPushButton {{ background-color: #42a5f5; color: white; font-size: {int(14 * scale_factor)}px; font-weight: bold; padding: {button_padding}; border-radius: 8px; border: none; }}
            QPushButton:hover {{ background-color: #2196f3; }}
        """)
        msg.exec()

    def remove_celebration_label(self):
        if self.celebration_label:
            effect = QGraphicsOpacityEffect()
            self.celebration_label.setGraphicsEffect(effect)
            fade_out = QPropertyAnimation(effect, b"opacity")
            fade_out.setDuration(500)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            
            def delete_label():
                if self.celebration_label:
                    self.layout.removeWidget(self.celebration_label)
                    self.celebration_label.deleteLater()
                    self.celebration_label = None
                    
            fade_out.finished.connect(delete_label)
            fade_out.start()

    def show_completion_message(self):
        # Hide unnecessary UI elements for cleaner look
        self.day_label.setText("🎉 סיום התוכנית! 🏆")
        self.save_button.hide()
        self.save_status.hide()
        self.plan_selector.setEnabled(False)
        
        # Hide checklist items
        for i in range(self.checklist_layout.count()):
            widget = self.checklist_layout.itemAt(i).widget()
            if widget:
                widget.hide()
                
        # Track completion count
        completion_count = self.progress.get("completion_count", 0) + 1
        self.progress["completion_count"] = completion_count
        save_progress(self.progress)
        
        # Animate new trophy being added to shelf
        if self.trophy_shelf:
            self.trophy_shelf.add_trophy_animated()
            
        # Wait for trophy animation to complete before showing popup
        QTimer.singleShot(1500, self.show_completion_popup)

    def show_completion_popup(self):
        # Grand celebration with intense confetti!
        if self.confetti:
            self.confetti.start_confetti(duration=8000, intensity=2.5)
            
        completion_count = self.progress.get("completion_count", 1)
        trophy_text = f"זה הפעם ה-{completion_count} שלך!" if completion_count > 1 else ""
        
        msg = QMessageBox(self)
        msg.setWindowTitle("🎊 מזל טוב! 🎊")
        msg.setText(
            f"🏆 כל הכבוד! 🏆\n\n"
            f"סיימת את כל התנ\"ך!\n"
            f"{trophy_text}\n\n"
            f"השגת הישג מדהים! 🌟\n"
            f"עכשיו זה הזמן המושלם\n"
            f"להתחיל מחדש ולחזק את הידע שלך!\n\n"
            f"לחץ OK להתחלת תוכנית חדשה 🚀"
        )
        
        # Scale font and dimensions based on window size
        scale_factor = min(self.width() / 600, self.height() / 600)
        font_size = int(20 * scale_factor)
        min_width = int(350 * scale_factor)
        padding = int(30 * scale_factor)
        button_padding = f"{int(15 * scale_factor)}px {int(40 * scale_factor)}px"
        
        msg.setStyleSheet(f"""
            QMessageBox {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff9c4, stop:0.5 #ffeb3b, stop:1 #fdd835); border: 4px solid #f9a825; border-radius: 20px; }}
            QMessageBox QLabel {{ font-size: {font_size}px; font-weight: bold; color: #f57f17; padding: {padding}px; min-width: {min_width}px; }}
            QPushButton {{ background-color: #4caf50; color: white; font-size: {int(16 * scale_factor)}px; font-weight: bold; padding: {button_padding}; border-radius: 10px; border: none; }}
            QPushButton:hover {{ background-color: #45a049; }}
        """)
        
        result = msg.exec()
        
        if result == QMessageBox.StandardButton.Ok:
            self.restart_plan_silently()

    def restart_plan_silently(self):
        """Restart plan without confirmation - used after completion"""
        if self.plan in self.progress:
            # Delete day progress, keep completion count
            temp_count = self.progress.get("completion_count", 0)
            del self.progress[self.plan] 
            self.progress["completion_count"] = temp_count
            
        self.day = 1
        self.progress[self.plan + "_day"] = self.day
        
        # Restore UI elements handled in update_checklist

        self.update_checklist()
        save_progress(self.progress)

    def restart_plan(self):
        """Restart plan with confirmation - used for manual restart"""
        confirm = QMessageBox.question(
            self, "איפוס", "האם אתה בטוח שברצונך להתחיל מחדש?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.restart_plan_silently()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.confetti:
            self.confetti.setGeometry(self.rect())
        if self.trophy_shelf:
            self.trophy_shelf.setGeometry(0, 0, self.width(), 80)

    def jump_to_last_day(self):
        """DEBUG: Jump to the last day of the current plan for testing"""
        self.day = len(PLANS[self.plan])
        self.progress[self.plan + "_day"] = self.day
        save_progress(self.progress)
        self.update_checklist()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TanachTracker()
    window.show()
    sys.exit(app.exec())