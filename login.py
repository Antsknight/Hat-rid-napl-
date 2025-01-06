import keyboard
from FelhasznaloClass import Felhasznalo


def Menu():
    asd = True
    print("Bejelentkezéshez nyomd meg a ,b, regisztrációhoz az ,r, betűt! ")
    while asd:
        try:  
            if keyboard.is_pressed('b'):  
               asd = False
               Bejelentkezes()
            elif keyboard.is_pressed('r'):
               asd = False
               Regisztracio()
        except:
            return

def Bejelentkezes():
    username = input("Adj meg egy felhasználó nevet: ")
    password = input("Add meg a jelszót: ")
    ellenorzes = open('felhasznalok.txt')
    for sor in ellenorzes:
        adatok = sor.strip().split(';')
        if adatok[1] == username and adatok[2] == password:
            return Felhasznalo(adatok[0],adatok[1],adatok[2])
        else:
            return Felhasznalo(-1,"Hiba nincs ilyen felhasználó","")

def Regisztracio():
    NewID = -1
    username = input("Adj meg egy felhasználó nevet: ")
    with open('felhasznalok.txt', 'r') as file:
        ellenorzes = file.readlines()
        sor = -1
        while sor+1 < len(ellenorzes):
            sor += 1
            adatok = ellenorzes[sor].strip().split(';')
            NewID = int(adatok[0])+1
            if adatok[1] == username:
                print("Ez a felhasználó név már létezik!")
                username = input("Adj meg egy felhasználó nevet: ")
                sor = -1
    password = input("Add meg egy jelszót: ")
    with open('felhasznalok.txt', 'a') as file: 
        file.write(f"\n{NewID};{username};{password}")
    print("Sikeres regisztráció!")
Menu()

"""
"""
