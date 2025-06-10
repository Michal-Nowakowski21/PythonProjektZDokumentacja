import random as r

def get_random_word():
    """
    Zwraca losowe słowo z pliku 'words.txt'.

    Plik 'words.txt' powinien znajdować się w katalogu, z którego uruchamiana jest aplikacja.

    :return: losowe słowo jako łańcuch znaków w formacie lowercase
    """
    with open("words.txt", "r", encoding="utf-8") as file:
        linie = file.readlines()
    wordNumber = int(r.random() * len(linie))  # dynamicznie dostosowuje się do długości pliku
    return linie[wordNumber].strip().lower()

def validate(userWord):
    """
    Waliduje słowo pod kątem długości i zawartości liter.

    :param userWord: słowo wpisane przez użytkownika
    :return: True jeśli słowo ma dokładnie 5 liter i składa się tylko z liter, False w przeciwnym razie
    """
    if len(userWord) != 5:
        print("Błąd: Słowo musi mieć 5 liter")
        return False
    if not userWord.isalpha():
        print("Błąd: Słowo składa się jedynie z liter")
        return False
    return True

def check_guess(userWord, trueWord):
    """
    Sprawdza trafienia liter w zgadywanym słowie względem słowa docelowego.

    Kolory zwracane jako lista 5 elementów odpowiadają literom:
    - "zielone" jeśli litera jest na właściwej pozycji
    - "żółte" jeśli litera jest w słowie, ale na innej pozycji
    - "szare" jeśli litera nie występuje w słowie

    :param userWord: słowo wpisane przez użytkownika
    :param trueWord: prawidłowe słowo do odgadnięcia
    :return: lista kolorów ["zielone", "żółte", "szare"] o długości 5 lub None jeśli walidacja nie przeszła
    """
    userWord = userWord.strip().lower()
    if not validate(userWord):
        return None

    tab = [""] * 5
    for i in range(len(userWord)):
        if userWord[i] == trueWord[i]:
            tab[i] = "zielone"
        elif userWord[i] in trueWord:
            tab[i] = "żółte"
        else:
            tab[i] = "szare"

    print(tab)
    return tab
