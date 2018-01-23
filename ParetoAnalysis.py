import pandas as pd
import matplotlib.pyplot as plt
from appJar import gui
global a
a = ""
def format_coord(x,y):
    return a

def onpick3(event):
    ind = event.ind
    global a
    a = "ID: ", ind[0]+4, "Name: ", method[ind[0]+2], "Value-x: ", x[ind[0]+2], "Value-y :", y[ind[0]+2]
    format_coord(x,y)
    
def plotpareto(btn):
    fig = plt.figure()
    global ax1
    global first
    global second
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel(first)
    ax1.set_ylabel(second)
    ax1.scatter(x[2:], y[2:], picker=True)
    for i in index:
        ax1.scatter(x[i], y[i], c = "r")
    fig.canvas.mpl_connect('pick_event', onpick3)
    ax1.format_coord = format_coord
    plt.show()

def close(btn):
    app.stop()
    
def compute(btn):
    global first
    global second
    first = app.getOptionBox("X axis")
    second = app.getOptionBox("Y axis")
    imp = app.getOptionBox("Implementation")
    global col1
    global col2
    col1 = col2 = imp
    if first == 'GC':
        if imp == 'P02':
            col1 = 'P02.1'
        if imp == 'P01':
            col1 = 'P01.1'
        if imp == 'Wille':
            col1 = 'Wille.1'
        if imp == 'ISM':
            col1 = 'ISM.1'
    if second == 'GC':
        if imp == 'P02':
            col2 = 'P02.1'
        if imp == 'P01':
            col2 = 'P01.1'
        if imp == 'Wille':
            col2 = 'Wille.1'
        if imp == 'ISM':
            col2 = 'ISM.1'
    if first == 'QC':
        if imp == 'P02':
            col1 = 'P02.2'
        if imp == 'P01':
            col1 = 'P01.2'
        if imp == 'Wille':
            col1 = 'Wille.2'
        if imp == 'ISM':
            col1 = 'ISM.2'
    if second == 'QC':
        if imp == 'P02':
            col2 = 'P02.2'
        if imp == 'P01':
            col2 = 'P01.2'
        if imp == 'Wille':
            col2 = 'Wille.2'
        if imp == 'ISM':
            col2 = 'ISM.2'

    xl = pd.read_excel("Treecover1.xlsx", na_values = '1000')
    global x
    global y

    x = list(xl[col1])
    y = list(xl[col2])
    global method
    method = list(xl['Methods'])

    minx = 9999
    temp = []

    i = 2
    while i < len(x):
        if int(x[i]) < minx and int(x[i]) != 0:
            temp.clear()
            temp.append(i)
            minx = x[i]
        elif int(x[i]) == minx:
            temp.append(i)
        i+=1

    miny = y[temp[0]]
    global index
    index = []
    for j in temp:
        if y[j] < miny and y[j] != 0:
            miny = y[j]
            index.clear()
            index.append(j)
        elif y[j] == miny:
            index.append(j)
            
def press(btn):
    filename = app.openBox(asFile = False , fileTypes=[('workbook', '*.xls'), ('workbook', '*.xlsx')])
    global p
    p = str(filename)
    print(p)

app = gui()
app.setTitle("Pareto")
app.setGeometry(500,200)
filemenus = ["Choose..."]
app.addMenuList("File", filemenus, press)
app.addMenuSeparator("File")
app.addMenuItem("File", "Exit", func = close)
priorities = ["L", "GC","QC"]
imps = ["P02", "P01", "Wille", "ISM"]
app.addLabel("l1","X axis",0,0)
app.addLabel("l2","Y axis", 0,2)
app.addOptionBox("X axis", priorities, 1, 0)
app.addOptionBox("Y axis", priorities, 1, 2)
app.addLabel("l3","Implementation",2,1)
app.addOptionBox("Implementation", imps,3,1)
app.addButton("Plot", plotpareto, 4, 2)
app.addButton("Compute", compute, 4, 0)
app.go()
