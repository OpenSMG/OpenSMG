from PySide.QtGui import QFrame, QLabel, QGridLayout, QLayout
import GLOBALS


class UiAboutFrame(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mainLayout = QGridLayout(self)

        self.versionLbl = QLabel("This is SMG version {version}".format(version=GLOBALS.VERSION))
        self.websiteLbl = QLabel("Follow <a href='https://martijnbrekelmans.com/SMG/smg_web.php'>this link to install the browser extension.</a>")
        self.supportLbl = QLabel("Mail smg@martijnbrekelmans.com for any questions. Make sure to include a screenshot of your problem.")

        self.mainLayout.addWidget(self.versionLbl, 0, 0)
        self.mainLayout.addWidget(self.websiteLbl, 1, 0)
        self.mainLayout.addWidget(self.supportLbl, 2, 0)

        self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.show()
