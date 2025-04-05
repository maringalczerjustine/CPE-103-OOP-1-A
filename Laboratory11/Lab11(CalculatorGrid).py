import tkinter as tk

root = tk.Tk()
root.title("Calculator")
root.configure(bg='lightblue')

entry = tk.Entry(root, width=15, font=('Arial', 24), bd=10, relief=tk.RIDGE, justify='right')
entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

def click(symbol):
    entry.insert(tk.END, symbol)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def clear():
    entry.delete(0, tk.END)

buttons = [
    ('C', 1, 0, clear),
    ('7', 2, 0, lambda: click('7')),
    ('8', 2, 1, lambda: click('8')),
    ('9', 2, 2, lambda: click('9')),
    ('/', 2, 3, lambda: click('/')),
    ('4', 3, 0, lambda: click('4')),
    ('5', 3, 1, lambda: click('5')),
    ('6', 3, 2, lambda: click('6')),
    ('*', 3, 3, lambda: click('*')),
    ('1', 4, 0, lambda: click('1')),
    ('2', 4, 1, lambda: click('2')),
    ('3', 4, 2, lambda: click('3')),
    ('-', 4, 3, lambda: click('-')),
    ('0', 5, 0, lambda: click('0')),
    ('.', 5, 1, lambda: click('.')),
    ('+', 5, 2, lambda: click('+')),
    ('=', 5, 3, calculate)
]

for (text, row, col, cmd) in buttons:
    tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
              command=cmd).grid(row=row, column=col, padx=2, pady=5)

root.mainloop()