import sys
import threading
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPlainTextEdit, QLineEdit
from PyQt6.QtCore import Qt

class EmittingStream:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.appendPlainText(text)
    
    def flush(self):
        pass

class ConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.console_output = QPlainTextEdit(self)
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("QPlainTextEdit { color: green; }")
        
        self.console_input = QLineEdit(self)
        self.console_input.setStyleSheet("QLineEdit { color: green; }")
        self.console_input.returnPressed.connect(self.on_enter)
        
        self.layout.addWidget(self.console_output)
        self.layout.addWidget(self.console_input)
        
        # Redirect stdout and stderr
        sys.stdout = EmittingStream(self.console_output)
        sys.stderr = EmittingStream(self.console_output)
        
    def on_enter(self):
        command = self.console_input.text()
        self.console_input.clear()
        self.execute_command(command)
    
    def execute_command(self, command):
        if command.startswith('cd '):
            self.change_directory(command[3:].strip())
        else:
            self.run_shell_command(command)
    
    def change_directory(self, path):
        try:
            os.chdir(path)
            self.console_output.appendPlainText(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            self.console_output.appendPlainText(f"Error: {str(e)}")

    def run_shell_command(self, command):
        try:
            # Determine shell command based on OS
            if os.name == 'nt':
                shell = True
            else:
                shell = False
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            if result.stdout:
                self.console_output.appendPlainText(result.stdout)
            if result.stderr:
                self.console_output.appendPlainText(result.stderr)
        except Exception as e:
            self.console_output.appendPlainText(f"Error: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    console_widget = ConsoleWidget()
    console_widget.show()
    
    # Example print statement to test redirection
    print("This should appear in the console widget.")
    
    sys.exit(app.exec())
