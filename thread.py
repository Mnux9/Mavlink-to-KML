import sys
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

lon = 0
import urllib.request, json, time, simplekml

kml = simplekml.Kml()
print('start')

pnt = kml.newpoint(name="Aircraft", description="Generic aircraft",
                coords=[(18.432314,-33.988862)])  # lon, lat, alt
pnt.altitudemode = simplekml.AltitudeMode.relativetoground #altitude
i = 0

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        global lon
        """Long-running task."""
        while True:

             # some JSON:
            with urllib.request.urlopen("http://127.0.0.1:56781/mavlink/") as url:
                y = json.load(url)
            lon = y["GPS_RAW_INT"]["msg"]["lon"] * 0.0000001
            pnt.coords=[(y["GPS_RAW_INT"]["msg"]["lon"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["lat"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["alt"] * 0.001) ]  # lon, lat optional height
            print(y["GPS_RAW_INT"]["msg"]["lon"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["lat"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["alt"] * 0.001) #serial print
            kml.save("pyout.kml")#update km
            sleep(1)
            self.progress.emit(lon)
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(format(lon))

    def runLongTask(self):
         # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())
