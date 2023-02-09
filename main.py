from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys,os, subprocess
from PyQt5.uic import loadUiType
from Bio import Align,SeqIO,AlignIO
from pairwise_alignment import pairwise_alignment
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Bullet_Graph import bulletgraph
from Bullet_Graph_Multiple import bulletgraph_Multiple
import panel as pn
import numpy as np
import panel.widgets as pnw
pn.extension()
from metrics import calculate_metrices
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Plot, Grid, Range1d
from bokeh.models.glyphs import Text, Rect
from bokeh.layouts import gridplot
import biotite.sequence as seq
import biotite.sequence.graphics as graphics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt
import biotite.sequence as seq
import biotite.sequence.align as align
import biotite.sequence.graphics as graphics
import time


ui,_ = loadUiType(os.path.join(os.path.dirname(__file__),'DNA_Alignment.ui'))

class DNA_Alignment_App(QMainWindow , ui):
    def __init__(self , parent=None):
        super(DNA_Alignment_App , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        #Global variables
        self.browse_bar_current_number = 1
        self.horizontalLayout_current_number = 12
        self.new_bar_list=[]
        self.txt_sequences=[]
        self.fasta_sequences=[]
        self.fasta_sequences_2=[]
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Error")
        
        # Grouping buttons
        self.alignment_type = QButtonGroup()
        self.alignment_type.setExclusive(True)  
        self.alignment_type.addButton(self.global_alignment,1)
        self.alignment_type.addButton(self.local_alignment,2)

        self.alignment_number = QButtonGroup()
        self.alignment_number.setExclusive(True)  
        self.alignment_number.addButton(self.pairwise_alignment,1)
        self.alignment_number.addButton(self.multi_alignment,2)

        self.browse_button_grp = QButtonGroup()
        self.browse_button_grp.addButton(self.browse_button_1)

        #set up buttons
        self.Handle_Buttons()
        self.global_alignment.setChecked(True)
        self.pairwise_alignment.setChecked(True)
        self.frame_8.hide()
        
    def Handle_Buttons(self):
        '''Initializing interface buttons'''
        self.browse_button_1.clicked.connect(self.Browse)
        self.calculate_button.clicked.connect(self.calculate)
        self.download_button.clicked.connect(self.download)
        self.add_file_button.clicked.connect(self.add_browse_bar)
        self.remove_file_button.clicked.connect(self.remove_file)
        self.representation_button.clicked.connect(self.next)
        self.back_button.clicked.connect(self.back)
        self.alignment_type.buttonClicked.connect(self.toggle)
        self.alignment_number.buttonClicked.connect(self.toggle)
        self.reset_button.clicked.connect(self.reset)
        self.dna_viewer_1.textEdited.connect(self.text_changed)

    def Browse(self):
        try:
            '''Browse for DNA sequence'''
            #Getting folder path
            dna_path = QFileDialog.getOpenFileName(self,"Select DNA FILE",directory='.')[0]
            if dna_path == '':
                return        
            _, file_extension = os.path.splitext(dna_path)
            # if file_extension =='.txt':
            #     self.flag =True
            #     dna = open(dna_path,'r').read()
            #     self.txt_sequences.append(dna)
            #     if self.browse_bar_current_number == 1:
            #         self.dna_viewer_1.setText(dna)
            #     else:
            #         self.new_dna_viewer.setText(dna) 
            if file_extension =='.fasta':
                # fasta_sequences = SeqIO.parse(open(dna_path),'fasta')
                # for fasta in fasta_sequences:
                #     print(fasta.seq)
                    # self.fasta_sequences_2.append(fasta.seq)
                self.path = dna_path
                # self.path=os.path.basename(os.path.normpath(dna_path))
                print(self.path)
                
                # muscle_result = subprocess.check_output(['muscle', "-align", in_file, "-output", out_file])
            
                
            
            else:
                dna_path=''
                return
        except:
                self.msg.setText("Browse a fasta File!")
                self.msg.exec_()  
    def text_changed(self):
        if self.pairwise_alignment.isChecked():
            if self.dna_viewer_1.text() !='':
                self.txt_sequences.append(self.dna_viewer_1.text())
                print('iiiiiiiiiiii')
    def text_changed_2(self):
        if self.pairwise_alignment.isChecked():
            if  self.new_dna_viewer.text() != '':
                self.txt_sequences.append(self.new_dna_viewer.text())
    
    def calculate(self):
        try:
            self.Seq1_Fig,self.Seq1_axes = self.canvas_setup(900,65,self.representation_view_1)
            self.Seq2_Fig,self.Seq2_axes = self.canvas_setup(900,65,self.representation_view_2)
            self.Seq3_Fig,self.Seq3_axes = self.canvas_setup(900,65,self.representation_view_3)
            self.Seq4_Fig,self.Seq4_axes = self.canvas_setup(900,65,self.representation_view_4)
            """ Align DNA sequence """
            self.metric_1_score.setValue(0.0)
            self.metric_2_score.setValue(0.0)
            self.metric_3_score.setValue(0.0)
            if self.global_alignment.isChecked():
                mode = 'global'
            else:
                mode = 'local'

            if self.pairwise_alignment.isChecked():
                self.Seq1_axes.clear()
                self.Seq2_axes.clear()
                self.Seq3_axes.clear()
                self.Seq4_axes.clear()
                match_score = 2
                mismatch_score = -1
                gap_score = -2
                print(self.txt_sequences)
                alignments, score = pairwise_alignment(self.txt_sequences[0].upper(), self.txt_sequences[1].upper(), mode, gap_score, match_score, mismatch_score)
                self.dna_result_viewer.clear()
                self.dna_result_viewer.setAlignment(Qt.AlignHCenter)
                self.dna_result_viewer.append(f"Score {score}")
                self.dna_result_viewer.append(str(alignments[0]))
                self.dna_result_viewer.append(str(alignments[1]))
                self.metric_1_score.setValue(score)
                #Representation
                
                sequence1 = alignments[0]
                sequence2 = alignments[1]
                Seq_1_List=self.Convert_To_List(sequence1)
                Seq_2_List=self.Convert_To_List(sequence2)
                # print(self.representation_view_1.

                
                axarr=[self.Seq1_axes,self.Seq2_axes]
                figarr=[self.Seq1_Fig,self.Seq2_Fig]
                data=[Seq_1_List,Seq_2_List]
                if(len(Seq_1_List)>len(Seq_2_List)):
                    size=len(Seq_1_List)
                else:
                    size=len(Seq_2_List)
                
                limits=list(range(1,size+1,1))
                bulletgraph(data, limits,
                    labels1=data[0],labels2=data[1],
                    bar_color="#252525", target_color='#f7f7f7',axarr=axarr,figarr=figarr)
            else:
                self.Seq1_axes.clear()
                self.Seq2_axes.clear()
                self.Seq3_axes.clear()
                self.Seq4_axes.clear()
                self.MultipleRepresentation()

                if self.browse_bar_current_number == 1:
                    self.dna_viewer_1.setText(str(self.align[0]))
                else:
                
                    self.new_dna_viewer.setText(str(self.fasta_sequences[0]))
                # p = self.view_alignment(self.align, plot_width=900)
                # pn.pane.Bokeh(p)
                for i in range(len(self.align)):
                    self.dna_result_viewer.append(str(self.align[i].seq))
                a,b,c = calculate_metrices(self.align)
                print(a,b,c)
                self.metric_1_score.setValue(a)
                self.metric_2_score.setValue(b)
                self.metric_3_score.setValue(c)
                
        except:
                self.msg.setText("Pick Correctly(Multiple,PairWise)!")
                self.msg.exec_()  
    def MultipleRepresentation(self):
        try:
            axarr=[self.Seq1_axes,self.Seq2_axes,self.Seq3_axes,self.Seq4_axes]
            figarr=[self.Seq1_Fig,self.Seq2_Fig,self.Seq3_Fig,self.Seq4_Fig]
        
            Multiple,size=self.MSA()
            data=Multiple
            limits=list(range(1,80,1))
            bulletgraph_Multiple(data, limits,
                labels1=data[0][1:80],labels2=data[1][1:80], labels3=data[2][1:80],lables4=data[3][1:80],multiple=True,
                bar_color="#252525", target_color='#f7f7f7',axarr=axarr,figarr=figarr)
        except:
                self.msg.setText("Error while using Multiple sequence!")
                self.msg.exec_()  
    def MSA(self):
        try:
            in_file = self.path
            out_file="Aligned_OutPut.fasta"

            muscle_result = subprocess.check_output(['muscle', "-align", in_file, "-output", out_file])
        

            self.align = AlignIO.read("Aligned_OutPut.fasta", "fasta")
            seqeuences=list()
            lengths=list()
            for i in range(len(self.align)):
                seqeuences.append(self.Convert_To_List(self.align[i].seq))
                lengths.append(len(seqeuences[i]))
            size=max(lengths)
        
            print(self.align)
        except:
                self.msg.setText("Error using Multiple sequeunce!")
                self.msg.exec_()        
        return seqeuences, size
    def download(self):
        try:
            
            '''Download result as a text file'''
            
            #open text file
            download_path = os.path.abspath(os.getcwd())+'\\result.txt'
            result_file = open(download_path, "w")
            
            #write string to file
            result_file.write(self.dna_result_viewer.toPlainText())
            
            #close file
            result_file.close()
        except:
                self.msg.setText("Error while downloading!")
                self.msg.exec_()     
    def reset(self):
        '''Reset Sequences'''
        self.txt_sequences.clear()
        self.fasta_sequences.clear()
        self.dna_result_viewer.clear()
        self.global_alignment.setChecked(True)
        self.local_alignment.setChecked(False)
        self.pairwise_alignment.setChecked(True)
        self.multi_alignment.setChecked(False)
        self.metric_1_score.setValue(0.0)
        self.metric_2_score.setValue(0.0)
        self.metric_3_score.setValue(0.0)
        
    def next(self):
        """move to the next tab"""
        self.tabWidget.setCurrentIndex(1)
    def back(self):
        """move to the previous tab"""
        self.tabWidget.setCurrentIndex(0)
            
    def toggle(self,obj):
        """Show or hide according to the selection"""
        if self.alignment_number.id(obj) ==1 : #if its pairwise only 1 metric will be used
            self.frame_8.hide()
        elif self.alignment_number.id(obj) ==2:
            self.frame_8.show()
            self.global_alignment.setChecked(True)
        if self.alignment_number.id(obj) ==2 : #if its multi alignment
            self.local_alignment.hide()
        elif self.alignment_number.id(obj) ==1:
            self.local_alignment.show()
            
    def Convert_To_List(self,string):
        list1 = []
        list1[:0] = string
        return list1  

    def canvas_setup(self,fig_width,fig_height,view,bool=True):
        '''Setting up a canvas to view an image in its graphics view'''
        scene= QGraphicsScene()
        figure = Figure(figsize=(fig_width/90, fig_height/90),dpi = 90)
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot()
        scene.addWidget(canvas)
        view.setScene(scene)
        if bool ==True:
            figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)
        else:
            axes.get_xaxis().set_visible(True)
            axes.get_yaxis().set_visible(True)
        return figure,axes
        


            
            
    def remove_file(self):
        """Remove file browse bar"""
        if len(self.new_bar_list) == 0:
            return
        self.new_bar_list[-1].deleteLater()
        self.new_bar_list.pop()
        if len(self.txt_sequences) >1:
            self.txt_sequences.pop()
        print(self.txt_sequences)
        self.browse_bar_current_number -= 1
        self.horizontalLayout_current_number -= 1
        
    def add_browse_bar(self):
        """Add browse bar to add file"""
        self.browse_bar_current_number+=1
        self.horizontalLayout_current_number+=1
        new_browse_bar_name = 'browse_frame_'+ str(self.browse_bar_current_number)
        new_horizontalLayout_name = 'horizontalLayout_'+ str(self.horizontalLayout_current_number)
        new_dna_viewer_name = 'dna_viewer_'+ str(self.browse_bar_current_number)
        browse_button_name = 'browse_button_'+ str(self.browse_bar_current_number)
                
        self.new_browse_bar_frame = QFrame(self.frame_3)
        self.new_bar_list.append(self.new_browse_bar_frame)
        self.new_browse_bar_frame.setObjectName(new_browse_bar_name)
        self.new_browse_bar_frame.setFrameShape(QFrame.NoFrame)
        self.new_browse_bar_frame.setFrameShadow(QFrame.Plain)
        self.new_horizontalLayout = QHBoxLayout(self.new_browse_bar_frame)
        self.new_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.new_horizontalLayout.setObjectName(new_horizontalLayout_name)
        self.new_dna_viewer = QLineEdit(self.new_browse_bar_frame)
        font = QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.new_dna_viewer.setFont(font)
        self.new_dna_viewer.setCursor(QCursor(Qt.IBeamCursor))
        self.new_dna_viewer.setMouseTracking(True)
        self.new_dna_viewer.setFocusPolicy(Qt.StrongFocus)
        self.new_dna_viewer.setAcceptDrops(False)
        self.new_dna_viewer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0,0,0);\n"
"")
        self.new_dna_viewer.setInputMask("")
        self.new_dna_viewer.setText("")
        self.new_dna_viewer.setFrame(True)
        self.new_dna_viewer.setEchoMode(QLineEdit.Normal)
        self.new_dna_viewer.setCursorPosition(0)
        self.new_dna_viewer.setAlignment(Qt.AlignCenter)
        self.new_dna_viewer.setDragEnabled(False)
        self.new_dna_viewer.setReadOnly(False)
        self.new_dna_viewer.setPlaceholderText("DNA " + str(self.browse_bar_current_number))
        self.new_dna_viewer.setClearButtonEnabled(False)
        self.new_dna_viewer.setObjectName(new_dna_viewer_name)
        self.new_horizontalLayout.addWidget(self.new_dna_viewer)
        _translate = QCoreApplication.translate
        self.new_browse_button = QPushButton(self.new_browse_bar_frame)
        self.new_browse_button.setText(_translate("MainWindow", "Browse"))
        self.new_browse_button.setObjectName(browse_button_name)
        self.new_browse_button.setEnabled(True)
        self.new_browse_button.setAutoFillBackground(False)
        self.new_browse_button.setStyleSheet("font: 12pt \"Broadway\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 85, 127);")
        self.new_horizontalLayout.addWidget(self.new_browse_button)
        self.verticalLayout_3.insertWidget(self.browse_bar_current_number-1,self.new_browse_bar_frame)
        print(new_dna_viewer_name)
        self.new_browse_button.clicked.connect(self.Browse)
        self.new_dna_viewer.textEdited.connect(self.text_changed_2)


        
            
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DNA_Alignment_App()
    window.show()
    app.exec_()