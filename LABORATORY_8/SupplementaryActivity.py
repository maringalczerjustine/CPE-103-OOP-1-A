import tkinter as tk
import math

def calculate(operation):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get()) \
            if entry2.get() else 0
        if operation == "add":
            res = num1 + num2
            add_to_history(f"{num1} + {num2} = {res}")
        elif operation == "subtract":
            res = num1 - num2
            add_to_history(f"{num1} - {num2} = {res}")
        elif operation == "multiply":
            res = num1 * num2
            add_to_history(f"{num1} × {num2} = {res}")
        elif operation == "divide":
            res = num1 / num2
            add_to_history(f"{num1} ÷ {num2} = {res}")
        elif operation == "sqrt":
            res = math.sqrt(num1)
            add_to_history(f"√{num1} = {res}")
        elif operation == "power":
            res = num1 ** num2
            add_to_history(f"{num1} ^ {num2} = {res}")
        result.set(res)
    except ValueError:
        result.set("Error! Invalid input.")
    except ZeroDivisionError:
        result.set("Error! Division by zero.")

def clear():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result.set("")

history = []
def add_to_history(operation):
    history.append(operation)
    history_label.config(text="\n".join(history[-5:]))  # Show last 5 operations

root = tk.Tk()
root.title("Simple Calculator")
root.configure(bg="lightblue")

result = tk.StringVar()

tk.Label(root, text="Enter first number:", bg="lightblue").grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="Enter second number:", bg="lightblue").grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

tk.Button(root, text="Add", command=lambda: calculate("add")).grid(row=2, column=0)
tk.Button(root, text="Subtract", command=lambda: calculate("subtract")).grid(row=2, column=1)
tk.Button(root, text="Multiply", command=lambda: calculate("multiply")).grid(row=3, column=0)
tk.Button(root, text="Divide", command=lambda: calculate("divide")).grid(row=3, column=1)
tk.Button(root, text="Square Root", command=lambda: calculate("sqrt")).grid(row=4, column=0)
tk.Button(root, text="Power", command=lambda: calculate("power")).grid(row=4, column=1)

tk.Button(root, text="Clear", command=clear).grid(row=5, column=0, columnspan=2)
tk.Label(root, text="Result:", bg="lightblue").grid(row=6, column=0)
tk.Label(root, textvariable=result, bg="white", font=("Arial", 12)).grid(row=6, column=1)

tk.Label(root, text="History:", bg="lightblue", anchor="w", justify="left").grid(row=7, column=0, columnspan=2)
history_label = tk.Label(root, text="", bg="white", font=("Arial", 10), anchor="w", justify="left")
history_label.grid(row=8, column=0, columnspan=2)

for widget in root.winfo_children():
    widget.configure(font=("Arial", 12), fg="black")

root.mainloop()
