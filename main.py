import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import ai_engine 

class AIWorker(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, text, mode):
        super().__init__()
        self.text = text
        self.mode = mode

    def run(self):
        # Passes both the clipboard text AND the selected option to our brain file
        result = ai_engine.ask_ollama(self.text, self.mode)
        self.finished_signal.emit(result)

class SocialGoodAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("AI Accessibility Companion for Social Good")
        self.resize(500, 500)
        
        layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget { background-color: #0F172A; color: #F8FAFC; font-family: 'Segoe UI', Arial; }
            QTextEdit { background-color: #1E293B; border: 2px solid #334155; border-radius: 8px; padding: 12px; font-size: 14px; color: #E2E8F0; }
            QComboBox { background-color: #1E293B; border: 2px solid #334155; border-radius: 8px; padding: 8px; color: #F8FAFC; font-size: 14px; }
            QPushButton { background-color: #2563EB; font-weight: bold; border-radius: 8px; padding: 12px; font-size: 14px; border: none; }
            QPushButton:hover { background-color: #3B82F6; }
            QPushButton:disabled { background-color: #1E293B; color: #64748B; }
        """)
        
        self.header_label = QLabel("✨ Copy text, choose your mode, and transform:")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 5px;")
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("Output text will appear here...")
        
        # New Feature: The Mode Dropdown Menu!
        self.mode_selector = QComboBox()
        self.mode_selector.addItem("Accessibility Summary", "Accessibility")
        self.mode_selector.addItem("🔥 Brainrot Translator", "Brainrot")
        
        self.action_btn = QPushButton("🧠 Process Clipboard Text")
        self.action_btn.clicked.connect(self.process_clipboard)
        
        layout.addWidget(self.header_label)
        layout.addWidget(self.mode_selector) # Insert dropdown visually
        layout.addWidget(self.text_display)
        layout.addWidget(self.action_btn)
        self.setLayout(layout)
        
    def process_clipboard(self):
        clipboard = QApplication.clipboard()
        copied_text = clipboard.text().strip()
        
        if not copied_text:
            self.text_display.setText("⚠️ Your clipboard is empty! Highlight and copy some text first.")
            return
            
        selected_mode = self.mode_selector.currentData()
        self.text_display.setText(f"⏳ Generating your {selected_mode} response...")
        self.action_btn.setEnabled(False)
        
        # Start background worker with chosen mode details
        self.worker = AIWorker(copied_text, selected_mode)
        self.worker.finished_signal.connect(self.on_ai_finished)
        self.worker.start()

    def on_ai_finished(self, result):
        self.text_display.setText(result)
        self.action_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialGoodAssistant()
    window.show()
    sys.exit(app.exec())
