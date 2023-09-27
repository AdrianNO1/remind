from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys, datetime, time, os, subprocess

hoverColorSheet = "background-color:rgb(173, 23, 155);"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.loadedUI = uic.loadUi(__file__.replace("PythonRemind.py", "remind.ui"), self)
        self.setWindowTitle("remind")
        self.orgColorSheet = [v for v in self.remind.styleSheet().split("\n") if "background-color" in v][0]
        self.error.setText("")
        self.reminderInitialized = False

        self.remind.leaveEvent = lambda x: self.remind.setStyleSheet(self.remind.styleSheet().replace(hoverColorSheet, self.orgColorSheet))
        self.remind.enterEvent  = lambda x: self.remind.setStyleSheet(self.remind.styleSheet().replace(self.orgColorSheet, hoverColorSheet))
        self.remind.pressed.connect(self.initiateReminder)

        self.date.insertPlainText("-".join(":".join(str(datetime.datetime.now()).split(":")[:2]).split(" ")[0].split("-")[::-1]))
        self.time.insertPlainText(":".join(str(datetime.datetime.now()).split(":")[:2]).split(" ")[1])

        self.show()
    

    def initiateReminder(self):
        if self.reminderInitialized:
            sys.exit()

        remindercount = int(open(__file__.replace("PythonRemind.py", "remindercount.txt"), "r").read()) + 1

        newfile = __file__.replace("PythonRemind.py", "reminders\\reminder" + str(remindercount) + ".txt")
        with open(newfile, "w") as f:
            f.write(f"{self.mainInput.toPlainText()}\n\nDATE:\n{self.date.toPlainText()}\n\nTIME:\n{self.time.toPlainText()}\n\nTime of creation:\n{str(datetime.datetime.now()).split('.')[0]}")
        
        pythonfile = newfile[:-3] + "pyw"
        with open(pythonfile, "w") as f:
            f.write(f'import os, sys\nos.system(r"{os.path.abspath(newfile)}")\nsys.exit()')
        
        pythonfile = os.path.realpath(pythonfile)
        
        code = os.system(fr'schtasks /create /tn "{"reminderTask" + open(__file__.replace("PythonRemind.py", "remindercount.txt"), "r").read()}" /tr "{pythonfile}" /sc once /sd {self.date.toPlainText().replace("-", "/")} /st {self.time.toPlainText()}')

        if code != 0:
            self.error.setText("ERROR CODE " + str(code))
            self.error.setStyleSheet("color:rgb(255, 0, 0);")
        else:
            self.error.setText("Task created succesfully!")
            self.error.setStyleSheet("color:rgb(0, 0, 255);")
            
            with open(__file__.replace("PythonRemind.py", "remindercount.txt"), "w+") as f:
                f.write(str(remindercount))

        self.remind.setText("Exit")
        self.reminderInitialized = True

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())