import time
import GameLogic  # moduł z logiką gry (losowanie słowa, sprawdzanie)
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk
import DB  # obsługa bazy danych wyników

COLORS = {
    "zielone": "#6aaa64",
    "żółte": "#c9b458",
    "szare": "#787c7e"
}
"""
Słownik mapujący nazwy kolorów na ich wartości HEX.
"""

# Zmienne globalne gry
guess = 0
won = False
trueWord = None  # Słowo do odgadnięcia (losowane przy starcie)
start = 0
entry = None
entry_var = None
user_nick = ""

def limit_entry_length(*args):
    """
    Ogranicza długość wpisanego tekstu w polu entry do maksymalnie 5 znaków.
    """
    global entry_var
    val = entry_var.get()
    if len(val) > 5:
        entry_var.set(val[:5])

def on_nick_enter(event):
    """
    Obsługuje naciśnięcie Enter w polu nick - uruchamia grę.
    """
    start_game()

def start_game():
    """
    Rozpoczyna grę:
    - pobiera nick z pola wpisywania
    - losuje słowo do zgadnięcia
    - przełącza widoki (ukrywa ekran startowy, pokazuje planszę)
    - ustawia fokus na pole do wpisywania słowa
    - startuje timer
    """
    global trueWord, start, user_nick

    user_nick = nick_entry.get().strip()
    if user_nick == "":
        return

    trueWord = GameLogic.get_random_word()

    start_frame.pack_forget()
    game_frame.pack(expand=True)
    entry.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    entry.focus_set()

    start = time.time()
    print(f"DEBUG: Wylosowane słowo: {trueWord}")

def checkWin(tab):
    """
    Sprawdza, czy gracz wygrał lub wykorzystał wszystkie próby.

    :param tab: lista kolorów ("zielone", "żółte", "szare") z ostatniego zgadnięcia
    """
    global won
    if all(color == "zielone" for color in tab):
        won = True
        end_game("Gratulacje! Wygrałeś!")
        end = time.time()
        DB.addUser(user_nick, won, int(end - start))
    elif guess == 6:
        end_game([f"Przegrałeś!", f"Poprawne słowo to {trueWord.upper()}"])
        end = time.time()
        DB.addUser(user_nick, won, int(end - start))

def end_game(messages):
    """
    Kończy grę i wyświetla końcowe komunikaty.

    :param messages: pojedynczy komunikat lub lista komunikatów do wyświetlenia
    """
    global start

    entry.config(state='disabled')

    for widget in root.winfo_children():
        widget.destroy()

    end_frame = ttk.Frame(root)
    end_frame.pack(expand=True)

    if isinstance(messages, list):
        for msg in messages:
            label = ttk.Label(end_frame, text=msg, font=("Helvetica", 24), bootstyle="danger")
            label.pack(pady=5)
    else:
        label = ttk.Label(end_frame, text=messages, font=("Helvetica", 24), bootstyle="success")
        label.pack(pady=20)

    time_taken = round(time.time() - start, 2)
    info_label = ttk.Label(end_frame, text=f"Nick: {user_nick}\nCzas: {time_taken}s", font=("Helvetica", 16))
    info_label.pack(pady=10)

    restart_button = ttk.Button(end_frame, text="Zagraj ponownie", command=restart_game, bootstyle="info-outline")
    restart_button.pack(pady=20)

def restart_game():
    """
    Resetuje zmienne i GUI, aby umożliwić rozpoczęcie nowej gry.
    """
    global guess, won, trueWord
    guess = 0
    won = False
    trueWord = None

    for widget in root.winfo_children():
        widget.destroy()

    init_gui()

def on_enter(event):
    """
    Obsługuje naciśnięcie Enter w polu wpisywania słowa:
    - pobiera słowo
    - wywołuje sprawdzenie zgadywania
    - koloruje pola
    - sprawdza warunek wygranej/przegranej
    """
    global guess, won, entry, entry_var
    if won:
        return

    slowo = entry_var.get().strip().lower()
    if len(slowo) != 5:
        return

    tab = GameLogic.check_guess(slowo, trueWord)
    if tab is None:
        return  # walidacja nie przeszła

    for i in range(5):
        labels[guess][i].config(text=slowo[i].upper())
        color = COLORS.get(tab[i], COLORS["szare"])
        frames[guess][i].config(bg=color)
        labels[guess][i].config(bg=color, fg="white")

    guess += 1
    entry_var.set("")
    checkWin(tab)

def init_gui():
    """
    Inicjalizuje główny interfejs GUI:
    - ekran startowy (nick + start)
    - planszę do gry (6 prób po 5 liter)
    - pole wpisywania słowa
    - ograniczenie długości pola do 5 znaków oraz filtrowanie liter
    """
    global root, start_frame, nick_entry, start_button, game_frame, entry, entry_var
    global frames, labels

    start_frame = ttk.Frame(root, padding=20)
    start_frame.pack(expand=True)

    welcome_label = ttk.Label(start_frame, text="Wpisz swój nick", font=("Helvetica", 20))
    welcome_label.pack(pady=10)

    nick_entry = ttk.Entry(start_frame, font=("Helvetica", 16))
    nick_entry.pack(pady=10)
    nick_entry.focus_set()
    nick_entry.bind("<Return>", on_nick_enter)

    start_button = ttk.Button(start_frame, text="Start", command=start_game, bootstyle="success")
    start_button.pack(pady=10)

    game_frame = ttk.Frame(root, padding=10)

    frames = []
    labels = []

    for j in range(6):  # 6 prób
        row_frames = []
        row_labels = []
        for i in range(5):  # 5 liter
            frame = tk.Frame(game_frame, width=60, height=60, bg="#d3d3d3", bd=2, relief="solid")
            frame.grid(row=j, column=i, padx=5, pady=5)
            frame.grid_propagate(False)

            label = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), bg="#d3d3d3", fg="white")
            label.place(relx=0.5, rely=0.5, anchor="center")

            row_frames.append(frame)
            row_labels.append(label)

        frames.append(row_frames)
        labels.append(row_labels)

    entry_var = tk.StringVar()
    entry_var.trace_add("write", limit_entry_length)

    def is_valid_char_input(char):
        # akceptuj tylko litery lub pusty string (usuwanie)
        return char.isalpha() or char == ""

    vcmd = root.register(lambda P: is_valid_char_input(P))

    entry = ttk.Entry(root, font=("Helvetica", 16), textvariable=entry_var,
                      validate="key", validatecommand=(vcmd, "%P"))
    entry.bind("<Return>", on_enter)

# Tworzymy i uruchamiamy okno gry
root = tb.Window(themename="flatly")
root.title("Wordle")
root.geometry("800x800")

init_gui()
root.mainloop()
