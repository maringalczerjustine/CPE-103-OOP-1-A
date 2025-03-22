import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

window = tk.Tk()
window.title('Birth Date & Gender Selector')
window.geometry('500x350')
window.iconbitmap('01769ec04b1cf37f07872e96b4d296ae.ico')
window.configure(bg="lightblue")

ttk.Label(window, text="Enter Your Details",
          background='white', foreground="light blue",
          font=("Times New Roman", 25)).grid(row=0, column=1, pady=10)

ttk.Label(window, text="Birth Month:",background='white',foreground=("light blue"), font=("Times New Roman", 12)).grid(column=0, row=1, padx=5, pady=5)
month_var = tk.StringVar()
month_combobox = ttk.Combobox(window, width=15, textvariable=month_var)
month_combobox['values'] = ('January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December')
month_combobox.grid(column=1, row=1)
month_combobox.current(0)

ttk.Label(window, text="Birth Date (DD):",background='white',foreground=("light blue"), font=("Times New Roman", 12)).grid(column=0, row=2, padx=5, pady=5)
date_var = tk.StringVar()
date_combobox = ttk.Combobox(window, width=5, textvariable=date_var)
date_combobox['values'] = tuple(range(1, 32))  # Days from 1 to 31
date_combobox.grid(column=1, row=2)
date_combobox.current(0)

ttk.Label(window, text="Birth Year (YYYY):",background='white',foreground=("light blue"), font=("Times New Roman", 12)).grid(column=0, row=3, padx=5, pady=5)
year_var = tk.StringVar()
year_combobox = ttk.Combobox(window, width=10, textvariable=year_var)
year_combobox['values'] = tuple(range(1900, 2025))  # Years from 1900 to 2024
year_combobox.grid(column=1, row=3)
year_combobox.current(100)  # Default to year 2000

ttk.Label(window, text="Select Gender:",background='white',foreground=("light blue"), font=("Times New Roman", 12)).grid(column=0, row=4, padx=5, pady=5)
gender_var = tk.StringVar()
gender_var.set("None")  # Default value

male_radio = ttk.Radiobutton(window, text="Male", variable=gender_var, value="Male")
female_radio = ttk.Radiobutton(window, text="Female", variable=gender_var, value="Female")

male_radio.grid(column=1, row=4, sticky="w")
female_radio.grid(column=1, row=5, sticky="w")

# Function to Show Selected Info
def show_birth_info():
    showinfo(
        title="Your Birth Details",
        message=f"You were born on {month_var.get()} {date_var.get()}, {year_var.get()}\nGender: {gender_var.get()}"
    )

submit_button = ttk.Button(window, text="Show Info", command=show_birth_info)
submit_button.grid(column=1, row=6, pady=15)

window.mainloop()