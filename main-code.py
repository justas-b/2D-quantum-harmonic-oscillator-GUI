from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import sys
import os
from scipy.special import hermite
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class MainWindow(QMainWindow):
    '''The main application class which inherits from its parent QMainWindow.'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Quantum Harmonic Oscillator Simulator") #sets the window title
        layout = QVBoxLayout() #sets layout to be a vertical box layout
        
        self.plot = Plotting() #defines a variable to obtain everything from the class 'Plotting@
        self.title = QLabel("2D Quantum Harmonic Oscillator") #sets a page title
        self.title.setStyleSheet('color:white')
        self.title.setAlignment(Qt.AlignCenter) #aligns the title to be at the centre
        self.title.setFont(QFont("SansSerif",25)) #sets font and font size of the title
        
        layout.addWidget(self.title) #adds the page title to the vertical box layout
        layout.addWidget(self.plot) #adds the Plotting class to the vertical box layout below the page title

        widget = QWidget()
        
        widget.setAutoFillBackground(True) 
        p = widget.palette()
        p.setColor(widget.backgroundRole(), Qt.black) #sets the color of the background
        widget.setPalette(p)        
        widget.setLayout(layout)
        self.setCentralWidget(widget) #sets the central widget

class PlotCanvas1(FigureCanvas):
    '''The first canvas class which is inherited from FigureClass. Used to set the layout of the first plot.'''
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        self.fig = Figure(figsize=(width,height),dpi=dpi,facecolor='black') #creates a figure space with a figure size and dpi
        FigureCanvas.__init__(self,self.fig)
        self.setupPlotAx1()
        
    def setupPlotAx1(self):
        '''Generates a subplot for the wave function.'''
        self.ax1 = self.fig.add_subplot(111, projection = "3d",facecolor='black') #creates a 3D subplot
        self.ax1.set_title("Wave function of $\psi_{n,m}$",color='white') #sets the title of the 1st subplot
        self.ax1.set_xlabel("Position of $\psi_{n}$",color='white') #sets x label
        self.ax1.set_ylabel("Position of $\psi_{m}$",color='white') #sets y label
        self.ax1.set_zlabel("$\psi_{n,m}$",color='white') #sets z label
        
class PlotCanvas2(FigureCanvas):
    '''The second canvas class which is inherited from FigureClass. Used to set the layout of the second plot.'''
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        self.fig = Figure(figsize=(width,height),dpi=dpi, facecolor='black')
        FigureCanvas.__init__(self,self.fig)
        self.setupPlotAx2()
        
    def setupPlotAx2(self):
        '''Generates a subplot for the probability distribution.'''
        self.ax2 = self.fig.add_subplot(111, projection = "3d",facecolor='black')  #creates a 3D subplot
        self.ax2.set_title("Probability distribution of $\psi_{n,m}$",color='white') #sets the title of the 2nd subplot
        self.ax2.set_xlabel("Position of $\psi_{n}$",color='white') #sets x label
        self.ax2.set_ylabel("Position of $\psi_{m}$",color='white') #sets y label
        self.ax2.set_zlabel("$|\psi_{n,m}|^{2}$",color='white') #sets z label
        
class PlotWidget1(QWidget):
    '''Creates a widget to store the wave function canvas.'''
    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
        self.canvas1 = PlotCanvas1(self) #defines canvas1 as the 'PlotCanvas1' class
        self.ax1 = self.canvas1.ax1 #calls ax1 from the 'PlotCanvas1' class
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout() #defines a vertical layout
        self.setLayout(layout) #sets the layout as the vertical layout defined above
        layout.addWidget(self.canvas1) #adds 'PlotCanvas1' as a widget to the vertical layout
        
    def clearCanvas(self):
        self.ax1.clear() #when clearCanvas is called its clears the first plot
        
    def update(self):
        self.canvas1.draw() #when update is called it updates the first plot with the new values
        
class PlotWidget2(QWidget):
    '''Creates a widget to store the probability distribution canvas.'''
    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
        self.canvas2 = PlotCanvas2(self) #defines canvas2 as the 'PlotCanvas2' class
        self.ax2 = self.canvas2.ax2 #calls ax2 from the 'PlotCanvas2' class
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout() #defines a vertical layout
        self.setLayout(layout) #sets the layout as the vertical layout defined above
        layout.addWidget(self.canvas2) #adds 'PlotCanvas2' as a widget to the vertical layout
        
    def clearCanvas(self):
        self.ax2.clear() #when ClearCanvas is called it clears the 2nd plot
        
    def update(self):
        self.canvas2.draw() #when update is called it updates the 2nd plot with the new values
        
class PlotButton(QWidget):
    '''Class which creates a button used to plot the graphs.'''
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self) #sets a vertical layout 
        self.button = QPushButton("Show!",self) #defines button as a QPushButton with the name 'Show!'
        self.button.setToolTip("Displays the wavefunction and the probability distribution plot.") #generates a tooltip which displays a phrase when you hover over the button
        self.layout.addWidget(self.button) #adds the button to the vertical layout
       
class InputValues(QWidget):
    '''Class used to generate the quantum numbers to be used in the data.'''
    def __init__(self,parent,label,inputType=QSpinBox):
        super(QWidget,self).__init__(parent)
        self.layout = QHBoxLayout() #defines a horizontal layout
        label = QLabel(label) #defines a label widget 
        label.setStyleSheet('color:white')
        self.input = inputType() #sets the input type as a QSpinBox widget 
        self.layout.addWidget(label) #adds the label widget to the layout
        self.layout.addWidget(self.input) #adds the input widget to the layout
        self.setLayout(self.layout) #sets the layout of the class as horizontal
        
    def setValue(self,value):
        '''Sets intial value when called.'''
        return self.input.setValue(value) 
        
    def value(self):
        '''Updates with new value when called.'''
        return self.input.value()
    
class Plotting(QWidget):
    '''Main class which houses the plots, buttons and tabs.'''
    def __init__(self):
        super().__init__()
        self.n = InputValues(self,"Quantum number n:") #sets 'self.n' as the 'InputValues' class which also adds the label to the spinbox    
        self.n.setToolTip("Alters the quantum number that corresponds to the wavefunction associated with X.") #sets a tooltip for 'self.n' to be displayed when you hover over the spinbox
        self.n.setValue(0) #calls 'setValue' from 'InputValues' which sets the initial value of 'self.n'
        self.m = InputValues(self,"Quantum number m:") #sets 'self.m' as the 'InputValues' class which also adds a label to the 2nd spinbox       
        self.m.setToolTip("Alters the quantum number that corresponds to the wavefunction associated with Y.") #adds a tooltip to 'self.m' to be displayed
        self.m.setValue(0) #sets the intial value of 'self.m'
        self.plotButton = PlotButton() #sets 'self.plotButton' as the 'PlotButton' class   
        
        infoTab = QTabWidget() #generates a 'QTabWidget'
        #sets as widgets
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        #defines the layout of the tabs
        tab1hbox = QHBoxLayout()
        tab2hbox = QHBoxLayout()
        tab3vbox = QVBoxLayout() 
        #sets the tab margins
        tab1hbox.setContentsMargins(5,5,5,5)     
        tab2hbox.setContentsMargins(5,5,5,5)  
        tab3vbox.setContentsMargins(5,5,5,5)
        #sets the layout of the tabs
        tab1.setLayout(tab1hbox)
        tab2.setLayout(tab2hbox)            
        tab3.setLayout(tab3vbox)
        #adds the tabs to QTabWidget and gives them labels
        infoTab.addTab(tab1, "Wave function")
        infoTab.addTab(tab2, "Probability") 
        infoTab.addTab(tab3, "LaTeX Report")  
        #generating the text to be displayed in the tabs           
        textEdit1 = QTextEdit("The solution of the wave function for the two-dimensional quantum harmonic\
                              oscillator (QHO) is determined by solving the time-independent Schrodinger\
                              equation for a harmonic potential which depends on angular frequency.\
                              If this is solved for a single positional argument, then we will only\
                              have a one-dimensional wave function with a single quantum number n. \
                              To obtain a two-dimensional wave function, we must take the product of two wave functions\
                              that only differ with positional variables and quantum numbers. We then have\
                              a wave function that depends on quantum numbers n and m in the x-y plane.\
                              By changing the quantum numbers, we can obtain plots of the wavefunction\
                              as shown in the first plot.") 
        textEdit2 = QTextEdit("We can use the two-dimensional wave function to determine the probability distribution\
                              of the particle. This is done by multiplying the expression for the wave function by\
                              its complex conjugate, which in this case is just the wave function since there is no\
                              time dependance. We can then change the quantum numbers to obtain plots of the probability\
                              distribution as a function of space. This is displayed in the seconds plot.") 
        textEdit3 = QTextEdit("I have included a LaTeX report that goes into more detail about the\
                              functionality and the physics behind my GUI.") 
        
        infoTab.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Preferred)        
        reportbutton = QPushButton("View report") #creates a button which will be used to launch the LaTeX report
        reportbutton.clicked.connect(self.open_report) #when the button is pressed it laun
        #sets the text to be read only so they cannot be edited, and sets the font and font size of the text
        textEdit1.setReadOnly(True) 
        textEdit1.setFont(QFont("SansSerif",13)) 
        textEdit2.setReadOnly(True) 
        textEdit2.setFont(QFont("SansSerif",13))
        textEdit3.setReadOnly(True) 
        textEdit3.setFont(QFont("SansSerif",13))
        #adding the text and the button to the corresponding tabs
        tab1hbox.addWidget(textEdit1) 
        tab2hbox.addWidget(textEdit2)
        tab3vbox.addWidget(textEdit3)
        tab3vbox.addWidget(reportbutton) 
                
        layoutG = QGridLayout() #setting a grid layout
        self.setLayout(layoutG) #setting the layout of the Plotting class as the grid layout
        #setting vertical and horizontal layouts
        layoutV = QVBoxLayout() 
        layoutH = QHBoxLayout()
        #adding the widgets to the horizontal layout and adding the horizontal layout to the vertical layout
        layoutH.addWidget(self.n)
        layoutH.addWidget(self.m)
        layoutH.addWidget(self.plotButton) 
        layoutV.addLayout(layoutH)
        #adding the QTabWidget to the grid layout at a given position and setting a vertical layout for the widgets contained within the vertical layout
        layoutG.addWidget(infoTab, 1,1,3,1)
        layoutG.addLayout(layoutV, 0,1)
        
        self.plotButton.button.clicked.connect(self.replot) #signal for when the plot button is clicked 
        #signals for when addPlotCanvas is called
        self.addPlotCanvas1(layoutG) 
        self.addPlotCanvas2(layoutG)
        
    def open_report(self):
        '''This opens the LaTeX report.'''
        os.startfile("Python_Project_Report.pdf")
        
    def addPlotCanvas1(self, layoutG):
        '''Adds a plot canvas to the grid layout defined in the class'''
        self.plotCanvas1 = PlotWidget1(self) #calls PlotWidget1 class
        self.plotCanvas1.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)  
        layoutG.addWidget(self.plotCanvas1,0,0,2,1) #adds the widget to the grid layout and positions it
        
    def addPlotCanvas2(self, layoutG):
        '''Adds a plot canvas to the grid layout defined in the class'''
        self.plotCanvas2 = PlotWidget2(self)  #calls PlotWidget2 class
        self.plotCanvas2.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)    
        layoutG.addWidget(self.plotCanvas2,2,0,2,1) #adds the widget to the grid layout and positions it
        
    def data(self, n, m, x, y):
        '''Function which generates the 2D QHO wave function data using the quantum numbers
        n,m and the positional arguments x,y'''
        #hermite polynomials using their respective quantum numbers
        h1 = hermite(n) 
        h2 = hermite(m)
        X, Y = np.meshgrid(x,y) #generates a X,Y plane using x,y values
        #generates the x and y dependent wave functions using the values given above
        fx = (h1(X)*np.exp(-(X**2)/2))/(np.sqrt((2**n)*(np.math.factorial(n))*(np.sqrt(np.pi))))
        fy = (h2(Y)*np.exp(-(Y**2)/2))/(np.sqrt((2**m)*(np.math.factorial(m))*(np.sqrt(np.pi))))
        f = fx*fy #works out the 2D wave function by working out the product of the fx and fy
        return X, Y, f #returns the positional values
        
    def replot(self):
        '''Function which replots the graphs when called'''
        #clears the canvas's before replotting
        self.plotCanvas1.clearCanvas()
        self.plotCanvas2.clearCanvas()
        #generates x,y,n,m values
        x = np.linspace(-5,5,200)
        y = np.linspace(-5,5,200)
        n = self.n.value() 
        m = self.m.value()
        #calling the data function which generates the positional values
        X = self.data(n,m,x,y)[0]
        Y = self.data(n,m,x,y)[1]
        Z = self.data(n,m,x,y)[2]
        #plotting the wave function with labels
        self.plotCanvas1.ax1.plot_surface(X, Y, Z, cmap='viridis',rstride=1, cstride=1,antialiased = False)
        self.plotCanvas1.ax1.set_title("Wavefunction of $\psi_{n,m}$",color='white')
        self.plotCanvas1.ax1.set_xlabel("Position of $\psi_{n}$",color='white')
        self.plotCanvas1.ax1.set_ylabel("Position of $\psi_{m}$",color='white')
        self.plotCanvas1.ax1.set_zlabel("$\psi_{n,m}$",color='white')
        self.plotCanvas1.canvas1.draw()
        #plotting the probability distribution with labels
        self.plotCanvas2.ax2.plot_surface(X, Y, Z**2, cmap='viridis',rstride=1, cstride=1,antialiased = False)
        self.plotCanvas2.ax2.set_title("Probability distribution of $\psi_{n,m}$",color='white')
        self.plotCanvas2.ax2.set_xlabel("Position of $\psi_{n}$",color='white')
        self.plotCanvas2.ax2.set_ylabel("Position of $\psi_{m}$",color='white')
        self.plotCanvas2.ax2.set_zlabel("$|\psi_{n,m}|^{2}$",color='white')
        self.plotCanvas2.canvas2.draw()
    
app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
