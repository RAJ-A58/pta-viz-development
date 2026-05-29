from PyQt6.QtCore import Qt
<<<<<<< HEAD
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication, QComboBox
from guiHelper import QSplitter, QLabel
=======
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication
from guiHelper import QSplitter
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
from gui_imageViewer import QLFCPAWidget, QCFGWindow
from gui_editor import QCodeEditorWindow
import sys
import json

class QApp(QWidget):
    def __init__(self, parent: QWidget | None=None):
        QWidget.__init__(self, parent)

        self.editor = QCodeEditorWindow(self.analyzeFunc)
        self.results = QLFCPAWidget()
        self.cfgWindow = QCFGWindow(self.results.setCurrStmt)

<<<<<<< HEAD
        # --- NEW: Dropdown to switch between Local and Global Scopes ---
        self.modeSelector = QComboBox()
        self.modeSelector.addItems(['LFCPA (Local View)', 'VASCO (Global View)'])
        self.modeSelector.currentIndexChanged.connect(self.analyzeFunc)

        topLayout = QHBoxLayout()
        topLayout.addWidget(QLabel("Analysis Scope:"))
        topLayout.addWidget(self.modeSelector)
        topLayout.addStretch()

        editorLayout = QVBoxLayout()
        editorLayout.addLayout(topLayout)
        editorLayout.addWidget(self.editor)
        
        editorContainer = QWidget()
        editorContainer.setLayout(editorLayout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(editorContainer)
=======
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.editor)
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        splitter.addWidget(self.cfgWindow)
        splitter.addWidget(self.results)

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter)
        self.setLayout(hbox)

    def changeAnalysisType(self, type:str):
<<<<<<< HEAD
        try:
            with open('./results/'+type+'/info.json') as f:
                infoDict = json.load(f)
            self.cfgWindow.resetData('./results/'+type+'/code.svg', infoDict['pos_dicts'])
            self.results.setData(infoDict['iters'])
        except FileNotFoundError:
            pass # Fails gracefully if results haven't been generated yet

    def analyzeFunc(self):
        # Read the dropdown and tell the viewer which folder to pull from
        if self.modeSelector.currentIndex() == 1:
            mode = 'vasco'
            self.results.setAnalysisMode('vasco')
        else:
            mode = 'lfcpa'
            self.results.setAnalysisMode('lfcpa')
            
        self.changeAnalysisType(mode)
=======
        with open('./results/'+type+'/info.json') as f:
            infoDict = json.load(f)
        self.cfgWindow.resetData('./results/'+type+'/code.svg', infoDict['pos_dicts'])
        self.results.setData(infoDict['iters'])

    def analyzeFunc(self):
        self.changeAnalysisType('lfcpa')
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089


if __name__ == '__main__':
    app = QApplication([])
<<<<<<< HEAD
    window = QApp()
    window.setWindowTitle('PTA-Viz Engine')
    window.resize(1800, 900)
=======
    window = QWidget()

    window = QApp()
    window.setWindowTitle('PTA-Viz')
    window.resize(1800, 900)

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    window.show()
    sys.exit(app.exec())