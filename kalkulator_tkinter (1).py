`~import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Kalkulator")
root.geometry("340x480")
root.resizable(False, False)
root.configure(bg="#202124")

expression = ""
display_var = tk.StringVar(value="0")

def update_display():
    display_var.set(expression if expression else "0")

def press(value):
    global expression
    if value == "C":
        expression = ""
    elif value == "⌫":
        expression = expression[:-1]
    elif value == "=":
        try:
            # Evaluasi hanya untuk operasi matematika dasar.
            allowed = set("0123456789+-*/.() ")
            if not expression or any(ch not in allowed for ch in expression):
                raise ValueError
            result = eval(expression, {"__builtins__": {}}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            expression = str(result)
        except ZeroDivisionError:
            expression = ""
            display_var.set("Tidak bisa dibagi 0")
            return
        except Exception:
            expression = ""
            display_var.set("Error")
            return
    elif value == "%":
        try:
            expression = str(eval(expression, {"__builtins__": {}}, {}) / 100)
        except Exception:
            expression = ""
            display_var.set("Error")
            return
    else:
        if display_var.get() in ("Error", "Tidak bisa dibagi 0"):
            expression = ""
        expression += value
    update_display()

display = tk.Entry(root, textvariable=display_var, font=("Arial", 28),
                   justify="right", state="readonly",
                   readonlybackground="#303134", fg="white",
                   bd=0, relief="flat")
display.pack(fill="x", padx=16, pady=(22, 18), ipady=18)

buttons = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""]
]
frame = tk.Frame(root, bg="#202124")
frame.pack(expand=True, fill="both", padx=12, pady=8)

for r, row in enumerate(buttons):
    for c, label in enumerate(row):
        if not label:
            continue
        value = {"÷": "/", "×": "*", "−": "-"}.get(label, label)
        if label in ("÷", "×", "−", "+"):
            bg, fg = "#f9ab00", "#202124"
        elif label == "=":
            bg, fg = "#8ab4f8", "#202124"
        elif label in ("C", "⌫", "%"):
            bg, fg = "#5f6368", "white"
        else:
            bg, fg = "#3c4043", "white"
        b = tk.Button(frame, text=label, font=("Arial", 18, "bold"),
                      bg=bg, fg=fg, activebackground="#777777",
                      bd=0, command=lambda v=value: press(v))
        span = 2 if label == "0" else 1
        b.grid(row=r, column=c, columnspan=span, sticky="nsew",
               padx=5, pady=5, ipady=13)

for r in range(5):
    frame.rowconfigure(r, weight=1)
for c in range(4):
    frame.columnconfigure(c, weight=1)

def keyboard_input(event):
    if event.char in "0123456789.+-*/":
        press(event.char)
    elif event.keysym == "Return":
        press("=")
    elif event.keysym == "BackSpace":
        press("⌫")
    elif event.keysym == "Escape":
        press("C")

root.bind("<Key>", keyboard_input)
root.mainloop()
