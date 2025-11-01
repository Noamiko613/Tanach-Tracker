import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QCheckBox, QPushButton, QScrollArea,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

def num_to_hebrew(num):
    hebrew_nums = [
        "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט",
        "י", "יא", "יב", "יג", "יד", "טו", "טז", "יז", "יח", "יט",
        "כ", "כא", "כב", "כג", "כד", "כה", "כו", "כז", "כח", "כט",
        "ל", "לא", "לב", "לג", "לד", "לה", "לו", "לז", "לח", "לט",
        "מ", "מא", "מב", "מג", "מד", "מה", "מו", "מז", "מח", "מט",
        "נ", "נא", "נב", "נג", "נד", "נה", "נו", "נז", "נח", "נט",
        "ס", "סא", "סב", "סג", "סד", "סה", "סו", "סז", "סח", "סט",
        "ע", "עא", "עב", "עג", "עד", "עה", "עו", "עז", "עח", "עט",
        "פ", "פא", "פב", "פג", "פד", "פה", "פו", "פז", "פח", "פט",
        "צ", "צא", "צב", "צג", "צד", "צה", "צו", "צז", "צח", "צט",
        "ק", "קא", "קב", "קג", "קד", "קה", "קו", "קז", "קח", "קט",
        "קי", "קיא", "קיב", "קיג", "קיד", "קטו", "קטז", "קיז", "קיח", "קיט",
        "קכ", "קכא", "קכב", "קכג", "קכד", "קכה", "קכו", "קכז", "קכח", "קכט",
        "קל", "קלא", "קלב", "קלג", "קלד", "קלה", "קלו", "קלז", "קלח", "קלט",
        "קמ", "קמא", "קמב", "קמג", "קמד", "קמה", "קמו", "קמז", "קמח", "קמט",
        "קנ"
    ]
    return hebrew_nums[num - 1] if 1 <= num <= 150 else str(num)

BOOKS = {
    "תורה": [("בראשית", 50), ("שמות", 40), ("ויקרא", 27), ("במדבר", 36), ("דברים", 34)],
    "נביאים": [
        ("יהושע", 24), ("שופטים", 21), ("שמואל א", 31), ("שמואל ב", 24),
        ("מלכים א", 22), ("מלכים ב", 25), ("ישעיהו", 66), ("ירמיהו", 52),
        ("יחזקאל", 48), ("הושע", 14), ("יואל", 4), ("עמוס", 9), ("עובדיה", 1),
        ("יונה", 4), ("מיכה", 7), ("נחום", 3), ("חבקוק", 3), ("צפניה", 3),
        ("חגי", 2), ("זכריה", 14), ("מלאכי", 4)
    ],
    "כתובים (ללא תהילים)": [
        ("משלי", 31), ("איוב", 42), ("שיר השירים", 8), ("רות", 4),
        ("איכה", 5), ("קהלת", 12), ("אסתר", 10), ("דניאל", 12),
        ("עזרא", 10), ("נחמיה", 13), ("דברי הימים א", 29), ("דברי הימים ב", 36)
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
        json.dump(progress, f, ensure_ascii=False)

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

class TanachTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("torah_icon.ico"))
        self.setWindowTitle("מעקב לימוד תנ\"ך")
        self.resize(600, 600)
        self.progress = load_progress()
        self.plan = self.progress.get("plan", "30 יום")
        self.day = self.progress.get(self.plan + "_day", 1)
        self.checkboxes = {}

        self.setup_ui()
        self.update_checklist()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)

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
#This is used to add a button to jump to the last day for debugging
        # self.jump_button = QPushButton("קפוץ ליום האחרון")
        # self.jump_button.clicked.connect(self.jump_to_last_day)
        # self.layout.addWidget(self.jump_button)

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
        for i in reversed(range(self.checklist_layout.count())):
            self.checklist_layout.itemAt(i).widget().deleteLater()

        self.day_label.setText(f"יום מספר: {self.day}")

        today = PLANS[self.plan].get(self.day, {})
        self.checkboxes = {}
        for category, text in today.items():
            checkbox = QCheckBox(f"{category}: {text}")
            checkbox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
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
            self.restart_button.hide()

    def toggle(self, category):
        day_data = self.progress.setdefault(self.plan, {}).setdefault(str(self.day), {})
        day_data[category] = self.checkboxes[category].isChecked()

    def save(self):
        self.progress["plan"] = self.plan
        self.progress[self.plan + "_day"] = self.day

        all_checked = all(cb.isChecked() for cb in self.checkboxes.values())
        if all_checked:
            self.day += 1
            self.progress[self.plan + "_day"] = self.day
            self.update_checklist()

        save_progress(self.progress)
        self.write_progress_txt()
        self.save_status.setText("✔️ התקדמות נשמרה בהצלחה!")

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

    def show_completion_message(self):
        self.day_label.setText("🎉 כל הכבוד! סיימת את כל התנ\"ך! 👏🎊")
        self.restart_button.show()

    def restart_plan(self):
        confirm = QMessageBox.question(self, "איפוס", "האם אתה בטוח שברצונך להתחיל מחדש?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            if self.plan in self.progress:
                del self.progress[self.plan]
            self.day = 1
            self.progress[self.plan + "_day"] = self.day
            self.update_checklist()
            save_progress(self.progress)

#This is used to jump to the day for debugging
    # def jump_to_last_day(self):
    #     self.day = len(PLANS[self.plan])
    #     self.progress[self.plan + "_day"] = self.day
    #     self.update_checklist()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TanachTracker()
    window.show()
    sys.exit(app.exec())
