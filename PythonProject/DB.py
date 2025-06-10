"""klasa do obslugi bazy danych"""
import sqlite3
conn = sqlite3.connect('BazaPython.db')#laczenie z baza
c = conn.cursor()
"""metoda do dodania uzytkownika"""
def addUser(nick, status, timeGame):
    c.execute("INSERT INTO Users (Nick, Status, TimeOfGame) VALUES (?, ?, ?)", (nick, status, timeGame))
    conn.commit()