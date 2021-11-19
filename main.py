import tkinter as tk
from tkinter import messagebox
import pyperclip
import webbrowser


FONT = ("Sans Serif", 11)


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
                if len(button_label) >= 80:
                    button_label = f"{button_label[:77]}..."

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
            #wraplength=470,
            font=FONT,
            width=70,
            height=1,
            command=self.copy_to_clipboard,
        )

    def copy_to_clipboard(self):
        pyperclip.copy(self.icd_nr)


class SearchFunctionality():
    def __init__(self, master, col, row):
        self.brave_url = "https://search.brave.com/search?q="
        self.google_url = "https://www.google.de/search?q="
        self.radiopaedia_url ="https://radiopaedia.org/search?lang=gb&scope=articles&q="
        self.width = 25

        self.entry = tk.Entry(width=self.width)
        self.entry.grid(column=col, row=row)

        self.button = tk.Button(master=master, text="Radiopaedia Search", width=self.width, font=FONT, command=self.radiopaedia_search)
        self.button.grid(column=col, row=row+1)
        self.button = tk.Button(master=master, text="Brave Search", width=self.width, font=FONT, command=self.brave_search)
        self.button.grid(column=col, row=row+2)
        self.button = tk.Button(master=master, text="Google Search", width=self.width, font=FONT, command=self.google_search)
        self.button.grid(column=col, row=row+3)

    def assemble_search_string(self, url):
        search_input = self.entry.get()
        search_input = "+".join(search_input.split(" "))
        search_url = f"{url}{search_input}"
        self.entry.delete(0, tk.END)
        return search_url

    def brave_search(self):
        search_url = self.assemble_search_string(url=self.brave_url)
        webbrowser.open(url=search_url, new=0)

    def google_search(self):
        search_url = self.assemble_search_string(url=self.google_url)
        webbrowser.open(url=search_url, new=0)

    def radiopaedia_search(self):
        search_url = self.assemble_search_string(url=self.radiopaedia_url)
        webbrowser.open(url=search_url, new=0)


def main():
    """The main function."""
    root = tk.Tk()
    root.title("Autotext Copy")

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
            all_buttons.append(CopyButton(root, text=b_text, icd_nr=icd_10))

        col = 0
        row = 0
        for button in all_buttons:
            button.grid(column=col, row=row)
            row += 1

    search = SearchFunctionality(master=root, col=1, row=0)

    root.mainloop()


if __name__ == "__main__":
    main()
