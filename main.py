import sys
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QLabel,QLineEdit,QFileDialog,QListWidget,QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import shutil


class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Pyqt5 T_Folder")
        #self.setWindowIcon(QIcon("Images/logo.ico"))
        self.background_color ="#0D1117"
        self.text_color = "#27CEFD"
        self.resize(800,550)
        #set window resaizbale attr to false :
        self.setFixedSize(480,600)
        self.move(200,60)
        # add image and titel to window :
        # image :
        self.label_titel_image = QLabel(self)
        self.label_titel_image.setPixmap(QPixmap("Images/icons8-ajouter-le-dossier-50.png"))
        # title :
        self.label_titel_message = QLabel(self)
        self.label_titel_message.setText("T_Folder (auto sort files) ")
        #body tools : label + textentry +btn_select_folder +btn_confirm:
        self.label_path_name = QLabel(self)
        self.label_path_name.setText("Folder path here :  ")
        self.entry_path = QLineEdit(self)
        self.entry_path.setPlaceholderText(" C:/Users/User_name/Documents/PYQt_Apps/app/src/....")
        self.btn_select_folder = QPushButton(self)
        self.btn_select_folder.setText("Open Folder")
        self.btn_start = QPushButton(self)
        self.btn_start.setText("Start")
        self.btn_select_folder.clicked.connect(self.select_folder)
        self.btn_start.clicked.connect(self.org_protocol)
        # add style for full window body :
        self.setStyleSheet("""
        background-color:"#0D1117";
        padding:0px;
        """)
        self.label_path_name.setStyleSheet("""
        color : "#27CEFD";
        font-size : 18px;
        """)
        self.label_titel_message.setStyleSheet("""
        color : "#27CEFD";
        font-size : 24px;
        text-decoration:underline;
        """)
        self.entry_path.setStyleSheet("""
        width:300px;
        height:25px;
        background-color:"#0D1117";
        border:1px solid #27CEFD;
        border-radius: 5px;
        color:"#27CEFD";
        """)
        self.btn_select_folder.setStyleSheet("""
        width:80px;
        height:17px;
        background-color:"#0D1117";
        border:1px solid #27CEFD;
        border-radius: 5px;
        color:"#27CEFD";
        """)
        self.btn_start.setStyleSheet("""
        width:80px;
        height:17px;
        background-color:"#0D1117";
        border:1px solid #27CEFD;
        border-radius: 5px;
        color:"#27CEFD";
        """)
        #move widget in window :
        self.label_titel_image.move(210,100)
        self.label_titel_message.move(120,170)
        self.label_path_name.move(120,250)
        self.entry_path.move(120,290)
        self.btn_select_folder.move(335,325)
        self.btn_start.move(375,575)
    # select and get files from folder selected :
    def select_folder(self):
        path = os.path.expanduser("~")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            self.path = dlg.selectedFiles()[0]
            self.entry_path.setText(self.path)
            #get folder : 
            opened_dir =os.listdir(self.path)
            #create a Qliste :
            self.liste_file = QListWidget(self)
            self.files_name = []
            for element in opened_dir:
                if os.path.isfile(self.path+"/"+str(element)):
                    self.liste_file.addItem(str(element))
                    self.files_name.append(element)
            #add to window:
            self.liste_file.setStyleSheet("""
            color: "#27CEFD";
            background-color:"#0D1117";
            width:300px;
            """)
            self.liste_file.move(120,370)
            self.liste_file.show()
        return
    def org_protocol(self):
        #1) detecte all extension :
        extensions = []
        for element in self.files_name:
            arr = element.split('.')
            if not arr[1] in extensions:
                extensions.append(arr[1])
        #2) create sub-folder for each extension : 
        liste_name = []
        for extension in extensions:
            name = "fichier-"+str(extension)
            if not name in os.listdir(self.path):
                os.mkdir(path=self.path+"/"+str(name), mode=777)
                liste_name.append(name)
        #3) copy file by extension:
        for name in liste_name:
            element = name.split('-')
            for fichier in os.listdir(self.path):
                extension = fichier.split('.')
                if os.path.isfile(self.path+"/"+str(fichier)):
                    if extension[1] == element[1]:
                        shutil.move(src=self.path+"/"+str(fichier), dst=self.path+"/"+str(name))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Task Completed ! ") 
        msg.setInformativeText("Open Folder in explorer ?")
        msg.setWindowTitle("Task Info !")
        text ='Folder/'
        for element in liste_name:
            text += "\n "+str(element)
        msg.setDetailedText(text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()
        return
    def msgbtn(self,i):
        if i.text() == "OK":
            #open folder in explorer:
            os.startfile(self.path)
        self.entry_path.setText('')
        self.liste_file.deleteLater()
        return
if __name__ == "__main__":
    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    fen = Fenetre()
    fen.show()
    app.exec_()