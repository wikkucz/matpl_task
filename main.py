import tkinter as tk
from tkinter import messagebox
import sqlite3


def create_table():
    with sqlite3.connect("fiszki.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS words (word TEXT PRIMARY KEY, translation TEXT)")


def add_word(word, translation):
    with sqlite3.connect("fiszki.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO words (word, translation) VALUES (?, ?)", (word, translation))
        conn.commit()


def check_translation():
    translation = entry_translation.get()
    if translation.lower() == current_word[1].lower():
        label_result.config(text="Brawo!", fg="green")
    else:
        label_result.config(text=f"Niepoprawna odpowiedź. Prawidłowe tłumaczenie to: {current_word[1]}", fg="red")


def next_word():
    load_next_word()
    label_result.config(text="")


def remove_word():
    if messagebox.askyesno("Usuwanie", "Czy na pewno chcesz to zrobić?"):
        with sqlite3.connect("fiszki.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM words WHERE word=?", (current_word[0],))
            conn.commit()
        next_word()


def update_word():
    new_translation = entry_translation.get()
    with sqlite3.connect("fiszki.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE words SET translation=? WHERE word=?", (new_translation, current_word[0]))
        conn.commit()
    label_result.config(text="Fiszka została poprawiona.")
    load_next_word()


def browse_database():
    with sqlite3.connect("fiszki.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM words")
        data = cursor.fetchall()
    browse_window = tk.Toplevel(root)
    browse_window.title("Przeglądanie bazy danych")
    for idx, word_data in enumerate(data, start=1):
        tk.Label(browse_window, text=f"{idx}. {word_data[0]} - {word_data[1]}").pack()


def load_next_word():
    global current_word
    with sqlite3.connect("fiszki.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1")
        current_word = cursor.fetchone()
    label_word.config(text=current_word[0])
    entry_translation.delete(0, tk.END)


root = tk.Tk()
root.title("Fiszki")
create_table()
current_word = None


label_word = tk.Label(root, text="", font=("Courier New", 20))
label_word.pack(pady=20)

entry_translation = tk.Entry(root, font=("Helvetica", 16))
entry_translation.pack(pady=10)

label_result = tk.Label(root, text="", font=("Arial", 14))
label_result.pack(pady=5)

button_check = tk.Button(root, text="Sprawdź", command=check_translation)
button_check.pack(pady=5)

button_next = tk.Button(root, text="Następne słówko", command=next_word)
button_next.pack(pady=5)

button_remove = tk.Button(root, text="Już umiem, usuń z bazy", command=remove_word)
button_remove.pack(pady=5)

button_update = tk.Button(root, text="Popraw fiszkę", command=update_word)
button_update.pack(pady=5)

button_browse = tk.Button(root, text="Przeglądaj bazę", command=browse_database)
button_browse.pack(pady=5)

# add_word("apple", "jabłko")
# add_word("dog", "pies")
# add_word("cat", "kot")
# add_word("red", "czerwony")
# add_word("green", "zielony")
# add_word("blue", "niebieski")

load_next_word()
root.mainloop()



from tkinter import Tk
root = Tk()
root.mainloop()