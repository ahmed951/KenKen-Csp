
import numpy as np
from kenkenClass import *
from tkinter import *

class KenKenGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) 
        
        self.size = 5
        self.generateSizeParameters()
        self.ex ,self.currentpuzzle , self.rects = parseGenerateOutput(self.size,self.step)

        
        size, cages = parse(self.ex)
        
        self.kenken = KenKen(size, cages)

        self.generateChoices()
        

        
        self.w = Canvas(master, width=502, height=503)
        self.w.pack()
        
        self.lblSize = Label(self, text="Size:", font="Arial 10 bold")
        self.lblSize.pack()
        mystr = StringVar()
        mystr.set(str(self.size))
        self.E1 = Entry(self, textvariable=mystr, width=5, bg="#888",
           fg="#fff")
        self.E1.pack()
        self.lblSize = Label(self, text="Algorithms: 1 for BT, 2 for FC, 3 for AC:", font="Arial 10 bold")
        self.lblSize.pack()
        algo = StringVar()
        algo.set("1")
        self.E2 = Entry(self, textvariable=algo, width=5, bg="#888",
           fg="#fff")
        self.E2.pack()
        
        self.lbl2 = Label(self, text="", font="Arial 10 bold")
        self.lbl2.pack()

        self.puzzle_widget() 

        
        self.movelist = np.zeros((self.size,self.size),dtype=np.int32).tolist()

        self.w.bind("<ButtonRelease-1>", self.change) 
        self.pack()

    def generateSizeParameters(self):
        self.step = 500 // self.size
        numberStepsY = [80,70,60,50,40,35,30]
        numberStepsX = [70,60,50,40,30,30,28]
        opStepsY = [20,20,20,20,15,15,15]
        opStepsX = [25,25,25,25,20,20,17]
        
        #self.step = steps[self.size - 3]
        self.numberStepY = numberStepsY[self.size - 3]
        self.numberStepX = numberStepsX[self.size - 3]
        self.opStepY = opStepsY[self.size - 3]
        self.opStepX = opStepsX[self.size - 3]

    def generateChoices(self):
        if(self.size == 3):
            self.choice = ['','1','2','3']
        if(self.size == 4):
            self.choice = ['','1','2','3','4']
        elif(self.size == 5):
            self.choice = ['','1','2','3','4','5']
        elif(self.size == 6):
            self.choice = ['','1','2','3','4','5','6']
        elif(self.size == 7):
            self.choice = ['','1','2','3','4','5','6','7']
        elif(self.size == 8):
            self.choice = ['','1','2','3','4','5','6','7','8']
        elif(self.size == 9):
            self.choice = ['','1','2','3','4','5','6','7','8','9']

    def puzzle_widget(self):

        self.w.create_rectangle(3, 3, 500, 500) 

        # Creates the puzzle board
        self.sqlist = []

        self.generateSizeParameters()

        maxY = self.opStepY + self.step * self.size
        for i in range(0, 500, self.step):
            for j in range(0, 500, self.step):
                x = j + self.step
                y = i + self.step
                self.sqlist.append(self.w.create_rectangle(j, i, x, y))

        fontSize1 = "20"
        fontSize2 = "20"
        if(self.size < 7 ):
            fontSize1 = "20"
            fontSize2 = "20"
        elif(self.size == 7 ):
            fontSize1 = "15"
            fontSize2 = "20"
        elif(self.size == 8 ):
            fontSize1 = "12"
            fontSize2 = "20"
        elif(self.size == 9):
            fontSize1 = "10"
            fontSize2 = "15"
        x = self.opStepX
        y = self.opStepY
        for element in self.currentpuzzle:
            self.w.create_text(x, y, font="Arial "+fontSize1 +" bold", text=element)
            y += self.step
            if y == maxY:
                y = self.opStepY
                x += self.step

        
        self.numbers = np.zeros((self.size,self.size),dtype=np.int32).tolist()

        x = self.numberStepX
        y = self.numberStepY
        for m in range(len(self.numbers)):
            for n in range(len(self.numbers)):
                self.numbers[m][n] = self.w.create_text(x, y, font="Arial " +fontSize2, text = self.choice[0])
                y += self.step
            y = self.numberStepY
            x += self.step

        #Buttons 
        self.buttonlist = []
        self.btn_generate = Button(self, text="Generate Puzzle")
        self.btn_generate.bind("<ButtonRelease-1>", self.generate)
        self.btn_generate.pack(side = LEFT, fill = X, expand = YES)
        self.buttonlist.append(self.btn_generate)
        
    def change(self, event):

        if(self.lbl2["text"]):
            self.lbl2["text"] = "" 

        #Updates the buttons to the current number
        row, column = self.kenken.changer(event,self.step)
        self.movelist[row][column] +=1 

        
        if self.movelist[row][column] > self.size: 
            self.movelist[row][column] = 0


        self.w.itemconfigure(self.numbers[row][column], text = self.choice[self.movelist[row][column]])


    def generate(self, event):
        
        if(len(Entry.get(self.E1))) :
            if(int(Entry.get(self.E1)) >= 3 and int(Entry.get(self.E1)) <= 9 ):
                
                self.size = int(Entry.get(self.E1))
                self.generateSizeParameters()
                self.ex ,self.currentpuzzle,self.rects = parseGenerateOutput(self.size,self.step)
                size, cages = parse(self.ex)
                self.kenken = KenKen(size, cages)
                self.numbers = np.zeros((self.size,self.size),dtype=np.int32).tolist()
                self.movelist = np.zeros((self.size,self.size),dtype=np.int32).tolist()
                
        
                self.generateChoices()
               
 
                self.lbl2["text"] = "Puzzle Generated"  
            else:
                self.lbl2["text"] = "Invalid size"
        else:
         self.lbl2["text"] = "Enter the size"