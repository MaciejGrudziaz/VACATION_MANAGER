from tkinter import *
from MainWindow import MainWindow
import RootEvents

root=Tk()

mainWnd=MainWindow(root)

#root.bind("<Configure>",lambda event : RootEvents.Resize(event.width,event.height,mainWnd))

menuBar=Menu(root)
menuBar.add_command(label="File",command=RootEvents.File)
menuBar.add_command(label="Edit",command=RootEvents.Edit)

root.config(menu=menuBar)

RootEvents.currentWidget=None
root.bind_all("<B1-Motion>",RootEvents.MouseLeftButtonMove)
root.bind_all("<Button-1>",RootEvents.MouseLeftButtonPressed)

root.mainloop()


