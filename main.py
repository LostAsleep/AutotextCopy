import tkinter as tk
import pyperclip


def get_button_data(fname="buttons.txt"):
    """Read the input file for the buttons."""
    button_data = []
    with open(fname) as f:
        for line in f:
            line = line.strip().split("|||")
            if len(line) != 2:
                continue
            temp = (" - ".join(line), line[0])
            button_data.append(temp)
    return button_data


class CopyButton(tk.Button):
    """Button class that is able to copy stuff to the clipboard."""

    def __init__(self, master, text, icd_nr):
        self.icd_nr = icd_nr
        super().__init__(
            master=master,
            text=text,
            wraplength=470,
            width=50,
            height=2,
            command=self.copy_to_clipboard,
        )

    def copy_to_clipboard(self):
        pyperclip.copy(self.icd_nr)


def main():
    """The main function."""
    root = tk.Tk()
    root.title("Autotext Copy")

    button_data = get_button_data()
    all_buttons = []
    for i in range(len(button_data)):
        b_text = button_data[i][0]
        icd_10 = button_data[i][1]
        all_buttons.append(CopyButton(root, text=b_text, icd_nr=icd_10))

    for button in all_buttons:
        button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
