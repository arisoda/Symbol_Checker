# symbol_checker_v2.py
import sys
import base64
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QDesktopWidget, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from icons_module import CHECK_BASE64, ALERT_BASE64


def load_icon(base64_data):
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(base64_data))
    return pixmap


def decode_emoji_hidden_text(s):
    lines = s.splitlines()
    decoded_lines = []
    for line in lines:
        decoded_bytes = []
        for char in line:
            cp = ord(char)
            if 0xFE00 <= cp <= 0xFE0F:
                decoded_bytes.append(cp - 0xFE00)
            elif 0xE0100 <= cp <= 0xE01EF:
                decoded_bytes.append(cp - 0xE0100 + 16)
        if decoded_bytes:
            try:
                decoded_lines.append(bytes(decoded_bytes).decode("utf-8"))
            except UnicodeDecodeError:
                decoded_lines.append("(invalid encoding)")
    return '\n'.join(decoded_lines)


class SymbolChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symbol Checker v2")
        self.resize(750, 320)
        self.center()
        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        font = QFont("Fira Code", 11)
        bold_font = QFont("Fira Code", 11)
        bold_font.setBold(True)

        self.text1 = QTextEdit()
        self.text2 = QTextEdit()
        self.text1.setFont(font)
        self.text2.setFont(font)

        self.count1 = QLabel("0")
        self.count2 = QLabel("0")
        self.count1.setFont(bold_font)
        self.count2.setFont(bold_font)
        self.count1.setAlignment(Qt.AlignCenter)
        self.count2.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setScaledContents(True)

        self.match_label = QLabel("")
        self.match_label.setFont(bold_font)

        match_layout = QHBoxLayout()
        match_layout.addWidget(self.icon_label)
        match_layout.addWidget(self.match_label)
        match_layout.setSpacing(8)

        self.check_button = QPushButton("Check")
        self.cancel_button = QPushButton("Cancel")

        self.check_button.clicked.connect(self.on_check)
        self.cancel_button.clicked.connect(self.close)
        self.text1.textChanged.connect(self.on_text_changed)
        self.text2.textChanged.connect(self.on_text_changed)

        self.text1.installEventFilter(self)
        self.text2.installEventFilter(self)

        left_box = QVBoxLayout()
        left_box.addWidget(self.count1)
        left_box.addWidget(self.text1)

        right_box = QVBoxLayout()
        right_box.addWidget(self.count2)
        right_box.addWidget(self.text2)

        text_layout = QHBoxLayout()
        text_layout.addLayout(left_box)
        text_layout.addLayout(right_box)

        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(match_layout)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.cancel_button)
        bottom_layout.addWidget(self.check_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(text_layout)
        self.main_layout.addLayout(bottom_layout)

        self.setLayout(self.main_layout)

    def update_counts(self):
        self.count1.setText(str(len(self.text1.toPlainText())))
        self.count2.setText(str(len(self.text2.toPlainText())))

    def check_match(self):
        s1 = self.text1.toPlainText()
        s2 = self.text2.toPlainText()

        decoded_msg1 = decode_emoji_hidden_text(s1)
        decoded_msg2 = decode_emoji_hidden_text(s2)

        # Remove existing decoded label if present
        if hasattr(self, 'decoded_layout'):
            self.main_layout.removeItem(self.decoded_layout)
            for i in reversed(range(self.decoded_layout.count())):
                item = self.decoded_layout.itemAt(i).widget()
                if item:
                    item.setParent(None)

        if decoded_msg1 or decoded_msg2:
            self.decoded1 = QLabel(f"Hidden:\n{decoded_msg1}" if decoded_msg1 else "")
            self.decoded2 = QLabel(f"Hidden:\n{decoded_msg2}" if decoded_msg2 else "")

            for lbl in (self.decoded1, self.decoded2):
                lbl.setFont(QFont("Fira Code", 10))
                lbl.setStyleSheet("color: #888;")
                lbl.setWordWrap(True)
                lbl.setAlignment(Qt.AlignTop)
                lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
                lbl.setMaximumWidth(self.width() // 2 - 40)

            self.decoded_layout = QHBoxLayout()
            self.decoded_layout.addWidget(self.decoded1)
            self.decoded_layout.addWidget(self.decoded2)
            self.main_layout.addLayout(self.decoded_layout)

        if s1 == s2:
            self.match_label.setText("MATCH")
            self.match_label.setStyleSheet("color: #2ecc71;")
            self.icon_label.setPixmap(load_icon(CHECK_BASE64))
            self.count1.setStyleSheet("color: #2ecc71;")
            self.count2.setStyleSheet("color: #2ecc71;")
        else:
            self.match_label.setText("NOT MATCH")
            self.match_label.setStyleSheet("color: #e74c3c;")
            self.icon_label.setPixmap(load_icon(ALERT_BASE64))
            self.count1.setStyleSheet("color: #e74c3c;")
            self.count2.setStyleSheet("color: #e74c3c;")

        if decoded_msg1 or decoded_msg2:
            h1 = self.decoded1.sizeHint().height()
            h2 = self.decoded2.sizeHint().height()
            max_h = max(h1, h2)
            
            w1 = self.decoded1.sizeHint().width()
            w2 = self.decoded2.sizeHint().width()
            max_w = max(w1, w2)
            
            self.decoded1.setMinimumHeight(max_h)
            self.decoded2.setMinimumHeight(max_h)
            self.decoded1.setMinimumWidth(max_w)
            self.decoded2.setMinimumWidth(max_w)



    def on_check(self):
        self.update_counts()
        self.check_match()

    def on_text_changed(self):
        self.update_counts()
        self.count1.setStyleSheet("")
        self.count2.setStyleSheet("")

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Tab:
                if source == self.text1:
                    self.text2.setFocus()
                    return True
                elif source == self.text2:
                    self.text1.setFocus()
                    return True
            elif event.key() == Qt.Key_Return and not event.modifiers():
                self.on_check()
                return True
            elif event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
                source.insertPlainText("\n")
                return True
        return super().eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SymbolChecker()
    window.show()
    sys.exit(app.exec_())
