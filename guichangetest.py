import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
x = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        global x
        self.button.setText(format(x))
        x = x + 1
        print(x)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
