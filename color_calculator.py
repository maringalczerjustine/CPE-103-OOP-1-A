from tkinter import *

class MyWindow:
    def __init__(self, win):
        win.configure(bg='#2C3E50') 

        self.lbl1 = Label(win, text='First number', fg='white', bg='#2C3E50', font=('Arial', 12, 'bold'))
        self.lbl2 = Label(win, text='Second number', fg='white', bg='#2C3E50', font=('Arial', 12, 'bold'))
        self.lbl3 = Label(win, text='Result', fg='white', bg='#2C3E50', font=('Arial', 12, 'bold'))

        self.t1 = Entry(win, bd=3, bg='#ECF0F1', font=('Arial', 12))
        self.t2 = Entry(win, bg='#ECF0F1', font=('Arial', 12))
        self.t3 = Entry(win, bg='#BDC3C7', font=('Arial', 12, 'bold'))

        self.btn1 = Button(win, text='Add', command=self.add, fg='white', bg='#27AE60', font=('Arial', 12, 'bold'))
        self.btn2 = Button(win, text='Subtract', command=self.sub, fg='white', bg='#C0392B', font=('Arial', 12, 'bold'))
        self.btn3 = Button(win, text='Multiply', command=self.multiply, fg='white', bg='#8E44AD', font=('Arial', 12, 'bold'))
        self.btn4 = Button(win, text='Clear', command=self.clear, fg='black', bg='#F1C40F', font=('Arial', 12, 'bold'))

        self.lbl1.place(x=100, y=50)
        self.t1.place(x=230, y=50, width=120, height=25)

        self.lbl2.place(x=100, y=100)
        self.t2.place(x=230, y=100, width=120, height=25)

        self.lbl3.place(x=100, y=150)
        self.t3.place(x=230, y=150, width=120, height=25)

        self.btn1.place(x=80, y=200, width=80, height=40)
        self.btn2.place(x=170, y=200, width=80, height=40)
        self.btn3.place(x=260, y=200, width=80, height=40)
        self.btn4.place(x=170, y=260, width=80, height=40)

    def add(self):
        self.t3.delete(0, 'end')
        num1 = int(self.t1.get())
        num2 = int(self.t2.get())
        result = num1 + num2
        self.t3.insert(END, str(result))

    def sub(self):
        self.t3.delete(0, 'end')
        num1 = int(self.t1.get())
        num2 = int(self.t2.get())
        result = num1 - num2
        self.t3.insert(END, str(result))

    def multiply(self):
        self.t3.delete(0, 'end')
        num1 = int(self.t1.get())
        num2 = int(self.t2.get())
        result = num1 * num2
        self.t3.insert(END, str(result))

    def clear(self):
        self.t1.delete(0, 'end')
        self.t2.delete(0, 'end')
        self.t3.delete(0, 'end')

window = Tk()
mywin = MyWindow(window)
window.title('Colorful Calculator')
window.geometry("450x350+10+10")
window.mainloop()
