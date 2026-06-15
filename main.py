import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import ai_engine 

# This class runs quietly in the background so the window never freezes
class AIWorker(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        # Run the AI processing in the background thread
        result = ai_engine.ask_ollama(self.text)
        self.finished_signal.emit(result)

class SocialGoodAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("AI Accessibility Companion for Social Good")
        self.resize(500, 450)
        
        layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget { background-color: #0F172A; color: #F8FAFC; font-family: 'Segoe UI', Arial; }
            QTextEdit { background-color: #1E293B; border: 2px solid #334155; border-radius: 8px; padding: 12px; font-size: 14px; color: #E2E8F0; }
            QPushButton { background-color: #2563EB; font-weight: bold; border-radius: 8px; padding: 12px; font-size: 14px; border: none; }
            QPushButton:hover { background-color: #3B82F6; }
            QPushButton:disabled { background-color: #1E293B; color: #64748B; }
        """)
        
        self.header_label = QLabel("✨ Copy complex text, then click below to make it accessible:")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 5px;")
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("Simplified, easy-to-read text will appear here...")
        
        self.action_btn = QPushButton("🧠 Simplify & Summarize Clipboard")
        self.action_btn.clicked.connect(self.process_clipboard)
        
        layout.addWidget(self.header_label)
        layout.addWidget(self.text_display)
        layout.addWidget(self.action_btn)
        self.setLayout(layout)
        
    def process_clipboard(self):
        clipboard = QApplication.clipboard()
        copied_text = clipboard.text().strip()
        
        if not copied_text:
            self.text_display.setText("⚠️ Your clipboard is empty! Highlight and copy some text first.")
            return
            
        self.text_display.setText("⏳ Thinking... breaking down the language for accessibility smoothly...")
        
        # Disable button so user can't spam click it while it thinks
        self.action_btn.setEnabled(False)
        
        # Start the background worker thread
        self.worker = AIWorker(copied_text)
        self.worker.finished_signal.connect(self.on_ai_finished)
        self.worker.start()

    def on_ai_finished(self, result):
        # Update text display and re-enable button when background thread finishes
        self.text_display.setText(result)
        self.action_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialGoodAssistant()
    window.show()
    sys.exit(app.exec())