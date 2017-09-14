from PySide.QtGui import QDialog, QLabel, QPushButton, QLineEdit, QHBoxLayout,\
    QVBoxLayout
from PySide.QtCore import Qt


class QRichTextDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # config
        self.resize(500, 100)

        # widgets
        self.okButton = QPushButton("Ok")
        self.cancelButton = QPushButton("Cancel")

        self.label = QLabel(self)
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(Qt.RichText)

        self.input = QLineEdit()

        # layout
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.okButton)
        self.buttonsLayout.addWidget(self.cancelButton)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.input)
        # self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonsLayout)

        # signals
        self.okButton.clicked.connect(self.okClicked)
        self.cancelButton.clicked.connect(self.cancelClicked)

    def setText(self, text):
        self.label.setText(text)

    def okClicked(self):
        self.accept()

    def cancelClicked(self):
        self.reject()

    def prompt(self):
        self.exec_()
        return (self.input.text(), self.result())
