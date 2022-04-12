#Author:    Spielberg Michel
#Date:      2/29/20

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPalette, QColor
import tkinter as tk
import tkinter.filedialog
import os, pathlib
from os import path
import sys

class myWin():
    base_dir = pathlib.Path(__file__).parent.resolve()
    
    

    def __init__(self):
        self.app = QApplication([])
        self.setTheme()
        
        
        self.ui = uic.loadUi(self.basePath('ui', 'MediaDialog.ui'))
        
        #tie functions to signals
        self.ui.nextButton.clicked.connect(self.signal_nextButton)
        self.ui.selectFiles.clicked.connect(self.signal_selectFiles)
        self.ui.renameFiles.clicked.connect(self.signal_renameFiles)
        self.ui.directoryButton.clicked.connect(self.signal_directoryButton)
        self.tk_root = None



        #end of tie functions
    def signal_nextButton(self):
        self.ui.mediaTab.setCurrentIndex((self.ui.mediaTab.currentIndex()+1) %2)

    def signal_selectFiles(self):
        """Return the list of files to be renamed"""
        #open a browseable window
        root = self.createTkWindow()
        files =  tk.filedialog.askopenfilenames(parent=root, title='Choose your files')
        #add files to list
        if(len(files)>0):
            self.ui.fileList.addItems(files)

    def signal_renameFiles(self):
        showname = self.ui.showName.text()
        season = self.ui.season.text()
        
        
        #verify each text box is not empty
        if(showname==""):
            self.ui.status.setText("Don't leave showname empty!")
            return
        elif(season==""):
            self.ui.status.setText("Don't leave season empty!")
            return
        try:
            int_season = int(season)
        except:
            self.ui.status.setText("Season is not a valid number!")
            return

        #split the episode range based on '-'
        
        #verify user selected some files
        if(self.ui.fileList.count()<1):
            self.ui.status.setText("You have to select files first, silly!")
            return


        #rename each file according to season tv show format on media servers
        for i in range(self.ui.fileList.count()):
            filename = self.ui.fileList.item(i)
            src = path.dirname(filename.text())
            file_extension = os.path.splitext(filename.text())[1]
            # print(src)
            # print(filename.text())
            #rename
            os.rename(filename.text(), src + "/" + showname + "-s" + season.zfill(2) + "e" + str(i+1).zfill(2) + file_extension)

        
        self.ui.status.setText("Success!")

        

        
    def signal_directoryButton(self):
        """Allow the user to select the root directory of the show"""   
        root = self.createTkWindow()
        folder_path = tk.filedialog.askdirectory(parent = root, title = "Choose your folder")
        print(folder_path)
        pass


    def showMe(self):
        self.ui.show()

    def exec(self):
        return self.app.exec()

    def createTkWindow(self):
        """Instantiate the tk root window and return the reference"""
        if(self.tk_root is None):
            self.tk_root =  tk.Tk()
            #hide the main window
            self.tk_root.withdraw()
        return self.tk_root
    
    def basePath(self, *args):
        """Return the full path of the folders and files\n
        Ex. "ui" and "file.ui" will return "basepath//ui//file.ui"
        """
        base_path = os.path.join(self.base_dir, args[0])
        for arg in args[1:]:
            base_path = os.path.join(base_path, arg)
        return base_path

    def setTheme(self):
        """Set the theme of the app"""
        self.app.setStyle('Fusion')
        self.app.setWindowIcon(QtGui.QIcon(self.basePath('icons', 'MainIcon.png')))
        palette = QPalette()
        #setting dark theme from https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(palette)
        palette
        
def main():
    mywin = myWin()
    mywin.showMe()
    sys.exit(mywin.exec())
    
   



if __name__ == "__main__":
    main()