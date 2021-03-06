#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 19:52:49 2017
Citation: https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/ 
@author: chengqiguo
"""
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showerror
import tkinter as tk
from pairDistance import *

def saveFile(fname, x1):
    if fname == None:
        popup('No file loaded!')
    else:
        x, y, distList = histogram1(fname, x=x1)
        for i in range(len(distList)):
            if (i + 1) % 4  == 0:
                distList[i] = str(distList[i]) + '\n'
            else:
                distList[i] = str(distList[i]) + '\t'
        name = asksaveasfile(mode='w',defaultextension='.txt')
        if fname == None:
            return 
        else:
            txt = ''.join(distList)
            name.write(txt)
            name.close


class pairDistanceFinder(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Pair Distance Finder')
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.fname = None
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save current Si-Si pair distance file', 
                             command=lambda: saveFile(self.fname, '0'))
        filemenu.add_command(label='Save current Si-O pair distance file', 
                             command=lambda: saveFile(self.fname, '1'))
        filemenu.add_command(label='Save current O-O pair distance file', 
                             command=lambda: saveFile(self.fname, '2'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='Save', menu=filemenu)

        tk.Tk.config(self, menu=menubar)
        
        
        self.frames = {}
        frame0 = StartPage(container, self)
        self.frames[StartPage] = frame0
        frame0.grid(row='0', column='0', sticky='nsew')
        for F in (SiSiDistance, SiODistance, OODistance):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row='0', column='0', sticky='nsew')
        self.show_frame(StartPage)
        
        #self.menu = tk.Menu(self)
        #self.config(menu=self.menu)
        #self.filemenu = tk.Menu(self.menu)
        #self.menu.add_cascade(label="File", menu=self.filemenu)
        #self.filemenu.add_command(label="New", command=lambda: loadFile)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def changefname(self, startpage):
        newName = self.frames[StartPage].getfname()
        self.fname = newName
        self.frames[SiSiDistance].changeName(newName)
        self.frames[SiODistance].changeName(newName)
        self.frames[OODistance].changeName(newName)
        
    def restoreName(self, sisidistance):
        self.frames[StartPage].restorefname()
        
    
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Welcome to the Histogram Plotter!')
        label.pack(pady=10, padx=10)
        self.fname = None
        self.controller = controller
        button0 = tk.Button(self, text='Load File', 
                            command=self.loadFile)
        button0.pack()

        button1 = tk.Button(self, text='Si-Si Pair Distance', 
                            command=lambda: controller.show_frame(SiSiDistance))
        button1.pack()
        
        button2 = tk.Button(self, text='Si-O Pair Distance', 
                            command=lambda: controller.show_frame(SiODistance))
        button2.pack()
        
        button3 = tk.Button(self, text='O-O Pair Distance', 
                            command=lambda: controller.show_frame(OODistance))
        button3.pack()
   
    def loadFile(self):
        self.fname = askopenfilename(initialdir = "/", title = "Select file",
                                     filetypes = (("txt files","*.txt"),
                                                  ("all files","*.*")))
        if self.fname == '':
            return
        else:
            self.controller.changefname(self)
    
    
    def getfname(self):
        return self.fname
        
    
    def restorefname(self):
        self.fname = None


def popup(msg):
    msg = msg
    popup = tk.Tk()
    popup.wm_title("Warning!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    button0 = tk.Button(popup, text="Okay", command = popup.destroy)
    button0.pack()
    popup.mainloop()

def maxwin(x, y):
    popup = tk.Tk()
    msg = "The maximum count is " + str(y) + ". Its corresponding distance(s) is(are) "\
          + str(x) + "."
    popup.wm_title(" ")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    button0 = tk.Button(popup, text="Okay", command = popup.destroy)
    button0.pack()
    popup.mainloop()
    
    
class SiSiDistance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Si-Si Pair Distance')
        label.pack(pady=10, padx=10)
        self.fname = None
        self.f = None
        self.canvas = None
        self.toolbar = None
        self.controller = controller
        self.popup = None
        button = tk.Button(self, text='Back', command=self.goBack)
        button.pack()
        button1 = tk.Button(self, text='Max values in count', 
                            command=lambda: maxwin(self.maximumX, self.maximumFreq))
        button1.pack()
        
    #def showMessage    
    
    def changeName(self, newName):
        if self.fname == None:
            self.fname = newName
            try:
                self.plot()
            except (RuntimeError, TypeError, ValueError, NameError):
                popup('There is no Silicon atom.')
        else:
            self.removePlot()
            self.fname = newName
            try:
                self.plot()
            except (RuntimeError, TypeError, ValueError, NameError):
                popup('There is no Silicon atom.')
                    
                
    def plot(self):
        self.f = Figure(figsize=(5, 5), dpi=100)
        x, y, distList = histogram1(self.fname, x='0')
        self.maximumFreq = max(y)
        self.maximumX = x[np.where(y==max(y))]
        a = self.f.add_subplot(111)
        a.set_xlabel('Distance(nm)')
        a.set_ylabel('Number')
        a.plot(x, y)
        self.f.suptitle('Si-Si Pair Distance', fontsize=14, fontweight='bold')
        self.f.subplots_adjust(top=0.85)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        
    def goBack(self):
        self.fname = None
        self.controller.show_frame(StartPage)
        self.controller.restoreName(self)
        self.removePlot()
    
    def removePlot(self):
        try:
            self.f.clear()
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()  
        except (RuntimeError, TypeError, AttributeError, ValueError, NameError):
            popup('Please load some file before plotting.')
        
        
        
class SiODistance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Si-O Pair Distance')
        label.pack(pady=10, padx=10)
        self.fname = None
        self.f = None
        self.canvas = None
        self.toolbar = None
        self.maximumFreq = None
        self.maximumX = None
        self.controller = controller
        button0 = tk.Button(self, text='Back', command=self.goBack)
        button0.pack()
        button1 = tk.Button(self, text='Max values in count', 
                            command=lambda: maxwin(self.maximumX, self.maximumFreq))
        button1.pack()
        
    def changeName(self, newName):
        if self.fname == None:
            self.fname = newName
            try:
                self.plot()
            except (RuntimeError, TypeError, ValueError, NameError):
                pass
        else:
            self.removePlot()
            self.fname = newName
            try:
                self.plot()
            except (RuntimeError, TypeError, ValueError, NameError):
                pass
    
    
    def plot(self):
        self.f = Figure(figsize=(5, 5), dpi=100)
        x, y, distList = histogram1(self.fname, x='1')
        self.maximumFreq = max(y)
        self.maximumX = x[np.where(y==max(y))]
        a = self.f.add_subplot(111)
        a.set_xlabel('Distance(nm)')
        a.set_ylabel('Number')
        a.plot(x, y)
        self.f.suptitle('Si-O Pair Distance', fontsize=14, fontweight='bold')
        self.f.subplots_adjust(top=0.85)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def goBack(self):
        self.fname = None
        self.controller.show_frame(StartPage)
        self.controller.restoreName(self)
        self.removePlot()
    
    def removePlot(self):
        try:
            self.f.clear()
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()  
        except (RuntimeError, TypeError, AttributeError, ValueError, NameError):
            popup('Please load some file before plotting.')
    
    
class OODistance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='O-O Pair Distance')
        label.pack(pady=10, padx=10)
        self.fname = None
        self.f = None
        self.canvas = None
        self.toolbar = None
        self.controller = controller
        self.maximumFreq = None
        self.maximumX = None
        button = tk.Button(self, text='Back', command=self.goBack)
        button.pack()
        button1 = tk.Button(self, text='Max values in count', 
                            command=lambda: maxwin(self.maximumX, self.maximumFreq))
        button1.pack()
     
    def changeName(self, newName):
        if self.fname == None:
            self.fname = newName
            try:
                self.plot()
            except (RuntimeError, TypeError, ValueError, NameError):
                popup('There is no Oxygen atom.')
        else:
            self.removePlot()
            self.fname = newName
            try:
                self.plot()
            except (RuntimeError, TypeError, ValueError, NameError):
                popup('There is no Oxygen atom.')
    
    def plot(self):
        self.f = Figure(figsize=(5, 5), dpi=100)
        x, y, distList = histogram1(self.fname, x='2')
        self.maximumFreq = max(y)
        self.maximumX = x[np.where(y==max(y))]
        a = self.f.add_subplot(111)
        a.set_xlabel('Distance(nm)')
        a.set_ylabel('Number')
        a.plot(x, y)
        self.f.suptitle('O-O Pair Distance', fontsize=14, fontweight='bold')
        self.f.subplots_adjust(top=0.85)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #text = tk.Text(self)
        #text.insert(END, "Just a text Widget\nin two lines\n")
    
    def goBack(self):
        self.fname = None
        self.controller.show_frame(StartPage)
        self.controller.restoreName(self)
        self.removePlot()
    
    def removePlot(self):
        try:
            self.f.clear()
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except (RuntimeError, TypeError, AttributeError, ValueError, NameError):
            popup('Please load some file before plotting.')


app = pairDistanceFinder()
app.geometry("720x720")
app.mainloop()
    
    