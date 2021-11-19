import tkinter as tk
from tkinter import messagebox
from functools import partial
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
            # wraplength=470,
            font=FONT,
            width=70,
            height=1,
            command=self.copy_to_clipboard,
        )

    def copy_to_clipboard(self):
        pyperclip.copy(self.icd_nr)


class SearchFunctionality:
    """Internet and MyHelios search buttons and link to my radio notes file."""

    def __init__(self, master, col, row):
        """Generate search UI parts upon initialization."""
        self.search_providers = {
            "Radiopaedia Search": "https://radiopaedia.org/search?lang=gb&scope=articles&q=",
            "Brave Search": "https://search.brave.com/search?q=",
            "Google Search": "https://www.google.de/search?q=",
            "Kodierhilfe Search": "https://www.kodierhilfe.de/icd/icd-10-gm/suche;type=alphabet;code=final;term=",
            "MyHelios Search": "https://myhelios.helios-gesundheit.de/suchergebnisse/?tx_heliossearch_search%5Bquery%5D=*",
        }

        self.width = 25
        self.current_row = row
        self.entry = tk.Entry(width=self.width, font=FONT)
        self.entry.grid(column=col, row=self.current_row)
        self.current_row += 1

        self.buttons = []

        for key, value in self.search_providers.items():
            # Needs partial because otherwise the function args
            # will not be correctly updated during iteration.
            button = tk.Button(
                master=master,
                text=key,
                width=self.width,
                font=FONT,
                command=partial(self.search_net, base_url=value),
            )
            button.grid(column=col, row=self.current_row)
            self.current_row += 1

        self.blank_label = tk.Label(text="", font=FONT)
        self.blank_label.grid(column=col, row=self.current_row)
        self.current_row += 1

        self.notes_button = tk.Button(
            master=master,
            text="My Radio Notes",
            width=self.width,
            font=FONT,
            command=partial(
                webbrowser.open,
                url="file:///G:/Radiologie/Radiologie-gesamt/09.%20Bilddaten-Ordner/Dissmann/08_notes/radiology-export.html",
                new=0,
            ),
        )
        self.notes_button.grid(column=col, row=self.current_row)
        self.current_row += 1

    def assemble_search_string(self, url):
        search_input = self.entry.get()
        search_input = "+".join(search_input.split(" "))
        search_url = f"{url}{search_input}"
        self.entry.delete(0, tk.END)
        return search_url

    def search_net(self, base_url):
        search_url = self.assemble_search_string(url=base_url)
        webbrowser.open(url=search_url, new=0)


def main():
    """The main function."""
    root = tk.Tk()
    root.title("Autotext Copy")
    root.resizable(False, False)

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
