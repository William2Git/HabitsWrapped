from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QSlider, QProgressBar, QComboBox, QListWidget, QRadioButton, QCheckBox, QHBoxLayout
# We will use Qt to align the label into the center, so its basic styling

from PySide6.QtCore import Qt
# create a child class MainWindows that inherits properties/methods from QMainWindow

import googleSheetsAPI as sheets

SPREADSHEET_ID = "1-MzR7upW3l2pUSEodxRXuzc3xt3v7rohWKbl1GO8nVg"
AVGSLEEP = "B3"
AVGGYM = "B4"
AVGBEDTIME = "D4"

class MainWindows(QMainWindow):

    def __init__(self):
        # running the initializer from QMainWindow
        super().__init__()
        self.setWindowTitle("HabitsWrapped")

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        
        # all statistic labels
        bedtime = QLabel(f"Average Bedtime: {sheets.get_values(SPREADSHEET_ID, AVGBEDTIME)["values"][0][0]}")
        bedtime.setAlignment(Qt.AlignCenter)
        sleepAvg = QLabel(f"Average Sleep: {sheets.get_values(SPREADSHEET_ID, AVGSLEEP)["values"][0][0]}")
        sleepAvg.setAlignment(Qt.AlignCenter)
        gymAvg = QLabel(f"Average Gym: {sheets.get_values(SPREADSHEET_ID, AVGGYM)["values"][0][0]}")
        gymAvg.setAlignment(Qt.AlignCenter)

        add = QPushButton("Add to sheet")
        add.clicked.connect(lambda: print("add"))

        remove = QPushButton("Remove from sheet")
        remove.clicked.connect(lambda: print("remove"))
        
        calculate = QPushButton("Calculate average sleep")
        calculate.clicked.connect(lambda: print("calculated!"))
        
        layout.addWidget(bedtime)
        layout.addWidget(sleepAvg)
        layout.addWidget(gymAvg)
        layout.addWidget(add)
        layout.addWidget(remove)
        layout.addWidget(calculate)
        
        
        

# Creates application object
app = QApplication()
# Creates MainWindow object, which contains teh actual window
window = MainWindows()
window.show()

app.exec()
