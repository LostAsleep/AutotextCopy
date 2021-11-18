import tkinter as tk
from tkinter import messagebox
import pyperclip


def get_button_data(fname="buttons.txt"):
    """Read the input file for the buttons."""
    button_data = []
    try:
        with open(file=fname, encoding="utf-8") as f:
            for line in f:
                line = line.strip().split("|||")
                if len(line) != 2:
                    continue

                button_label = line[0]
                button_label = button_label.strip()
                if len(button_label) > 100:
                    button_label = f"{button_label[:-3]}..."

                to_clipboard = line[1]
                to_clipboard = to_clipboard.strip()

                temp = (button_label, to_clipboard)
                button_data.append(temp)
        return button_data
    except FileNotFoundError:
        return None


class CopyButton(tk.Button):
    """Button class that is able to copy stuff to the clipboard."""

    def __init__(self, master, text, icd_nr):
        self.icd_nr = icd_nr

        super().__init__(
            master=master,
            text=text,
            width=60,
            height=2,
            font=("Arial", 12),
            wraplength=500,
            padx=12,
            pady=2,
            command=self.copy_to_clipboard,
        )

    def copy_to_clipboard(self):
        pyperclip.copy(self.icd_nr)


def main():
    """The main function."""
    root = tk.Tk()
    root.title("Autotext Copy")
    root.configure(height=100, width=490)
    root.maxsize(height=100)
    root.pack_propagate(0)

    canvas = tk.Canvas(root)
    canvas.pack()

    main_frame = tk.Canvas(canvas)
    main_frame.pack(side="left", fill="both")

    myscrollbar = tk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right")

    button_data = get_button_data()
    if button_data is None:
        messagebox.showerror(
            title="No Button Data", message="No file named 'buttons.txt' was found"
        )
        root.destroy()
    else:
        all_buttons = []
        for i in range(len(button_data)):
            b_text = button_data[i][0]
            icd_10 = button_data[i][1]
            all_buttons.append(CopyButton(main_frame, text=b_text, icd_nr=icd_10))

        for button in all_buttons:
            button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
