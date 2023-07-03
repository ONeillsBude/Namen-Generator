import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import os

class NameGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Namen Generator")

        self.language_prefixes = {
            "Deutsch": "[DE]",
            "Englisch": "[EN]",
            "Französisch": "[FR]",
            "Japanisch": "[JP]",
        }

        self.gender_prefixes = {
            "Männlich": "[M]",
            "Weiblich": "[W]"
        }

        self.first_names_file = ""
        self.last_names_file = ""

        self.create_widgets()

        # Standardmäßig "Deutsch" und "Männlich" auswählen
        self.language_var.set("Deutsch")
        self.gender_var.set("Männlich")
        self.update_files()
        
        self.version_label = ttk.Label(self.root, text="0.1.2.0", foreground="gray", font=("Arial", 10))
        self.version_label.place(x=window_width-80, y=window_height-30)
        
        root.resizable(False, False)

    def create_widgets(self):
        # Sprachauswahl
        self.language_label = ttk.Label(self.root, text="Namen Sprache:")
        self.language_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.OptionMenu(self.root, self.language_var, "", *self.language_prefixes.keys(), command=self.update_files)
        self.language_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Geschlechtsauswahl
        self.gender_label = ttk.Label(self.root, text="Geschlecht:")
        self.gender_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.OptionMenu(self.root, self.gender_var, "", *self.gender_prefixes.keys(), command=self.update_files)
        self.gender_dropdown.grid(row=0, column=3, padx=5, pady=5)

        # Vornamen-Eingabefeld
        self.first_name_label = ttk.Label(self.root, text="Vorname:")
        self.first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.first_name_entry = ttk.Entry(self.root)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Nachnamen-Eingabefeld
        self.last_name_label = ttk.Label(self.root, text="Nachname:")
        self.last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.last_name_entry = ttk.Entry(self.root)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5)

        # Speichern Button
        self.save_button = ttk.Button(self.root, text="Speichern", command=self.save_names)
        self.save_button.grid(row=2, column=2, padx=5, pady=5, sticky="n")

        # Generiere Namen Button
        self.generate_button = ttk.Button(self.root, text="Generiere Namen", command=self.generate_names)
        self.generate_button.grid(row=3, column=1, padx=5, pady=5)

        # Textfeld für generierte Namen
        self.generated_names_text = tk.Label(self.root, text="", wraplength=400, justify="center")
        self.generated_names_text.grid(row=4, column=0, columnspan=4, padx=5, pady=10)

        self.first_name_status = tk.StringVar()
        self.first_name_status.set("")  # Der Standardwert ist leer

        self.first_name_status_text = tk.Label(self.root, textvariable=self.first_name_status)
        self.first_name_status_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.last_name_status = tk.StringVar()
        self.last_name_status.set("")  # Der Standardwert ist leer

        self.last_name_status_text = tk.Label(self.root, textvariable=self.last_name_status)
        self.last_name_status_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.bind_enter_key()

    def update_files(self, *args):
        language = self.language_var.get()
        gender = self.gender_var.get()

        prefix = self.language_prefixes.get(language, "")
        gender_prefix = self.gender_prefixes.get(gender, "")

        self.first_names_file = f"Namen/{prefix}Vornamen{gender_prefix}.txt"
        self.last_names_file = f"Namen/{prefix}Nachnamen.txt"

        # Erstelle den Ordner "Namen", falls er nicht existiert
        if not os.path.exists("Namen"):
            os.makedirs("Namen")

        # Erstelle die Dateien, wenn sie nicht existieren
        if not self.check_file_exists(self.first_names_file):
            self.create_names_file(self.first_names_file)
        
        if not self.check_file_exists(self.last_names_file):
            self.create_names_file(self.last_names_file)

    def generate_names(self):
        first_names = self.load_names_from_file(self.first_names_file)
        last_names = self.load_names_from_file(self.last_names_file)

        if not first_names or not last_names:
            self.generated_names_text.config(text="Es wurden keine Namen gefunden.")
            self.first_name_status.set("")  # Leere den Vorname-Status-Text
            self.last_name_status.set("")  # Leere den Nachname-Status-Text
            return

        generated_first_name = random.choice(first_names)
        generated_last_name = random.choice(last_names)

        generated_name = f"Vollständiger Name: {generated_first_name} {generated_last_name}"
        self.generated_names_text.config(text=generated_name)
        self.first_name_status.set("")  # Leere den Vorname-Status-Text
        self.last_name_status.set("")  # Leere den Nachname-Status-Text
       
    def load_names_from_file(self, file_name):
        try:
            with open(file_name, "r", encoding="latin-1") as file:
                names = [line.strip() for line in file]
                return names
        except UnicodeDecodeError:
            print("Fehler beim Lesen der Datei mit Zeichenkodierung 'latin-1'.")
            return []

    def check_file_exists(self, file_name):
        return os.path.exists(file_name)

    def create_names_file(self, file_name):
        try:
            with open(file_name, "w", encoding="utf-8"):
                pass
        except IOError:
            self.error_text.config(text="Fehler beim Erstellen der Datei.")

    def save_names(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()

    # Vorname
        if not first_name:
            self.first_name_status.set("")  # Leere den Status-Text, wenn keine Eingabe vorhanden ist 
        
        if first_name:
            try:
                with open(self.first_names_file, "r+") as f:
                    existing_first_names = [name.strip() for name in f.readlines()]

                    if first_name not in existing_first_names:
                        f.write(f"{first_name}\n")
                        self.first_name_status.set("Vorname gespeichert")
                    else:
                        self.first_name_status.set("Vorname existiert bereits")
            except FileNotFoundError:
                with open(self.first_names_file, "w") as f:
                    f.write(f"{first_name}\n")
                    self.first_name_status.set("Vorname gespeichert")

            self.first_name_entry.delete(0, 'end')  # Eingabefeld leeren
            
            self.generated_names_text.config(text="") # Leere den generierten Namenstext

    # Nachname
        if not last_name:
            self.last_name_status.set("")  # Leere den Status-Text, wenn keine Eingabe vorhanden ist
        
        if last_name:
            try:
                with open(self.last_names_file, "r+") as f:
                    existing_last_names = [name.strip() for name in f.readlines()]

                    if last_name not in existing_last_names:
                        f.write(f"{last_name}\n")
                        self.last_name_status.set("Nachname gespeichert")
                    else:
                        self.last_name_status.set("Nachname existiert bereits")
            except FileNotFoundError:
                with open(self.last_names_file, "w") as f:
                    f.write(f"{last_name}\n")
                    self.last_name_status.set("Nachname gespeichert")

            self.last_name_entry.delete(0, 'end')  # Eingabefeld leeren
                
            self.generated_names_text.config(text="") # Leere den generierten Namenstext

    def bind_enter_key(self):
        self.first_name_entry.bind("<Return>", lambda event: self.save_names())
        self.last_name_entry.bind("<Return>", lambda event: self.save_names())

root = tk.Tk()
window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
app = NameGeneratorApp(root)
root.mainloop()