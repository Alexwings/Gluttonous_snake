import threading
from PyQt6.QtWidgets import QMessageBox
class MessageRouter:
    def __init__(self) -> None:
        self.alert_message = threading.Condition()
    
    def show_alert(self, message: str, title: str):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        # message_box.setDefaultButton(QMessageBox.standardButton.OK)
        message_box.exec()

router = MessageRouter()