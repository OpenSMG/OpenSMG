from PySide.QtGui import QDialog

class ErrorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
