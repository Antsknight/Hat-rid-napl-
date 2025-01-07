import keyboard
import os
import json
import time
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
    with open('felhasznalok.txt', 'r') as file:
        for sor in file:
            adatok = sor.strip().split(';')
            if adatok[1] == username and adatok[2] == password:
                print("Sikeres bejelentkezés!")
                user = Felhasznalo(adatok[0], adatok[1], adatok[2])
                UserMenu(user)
                return
    print("Hiba: nincs ilyen felhasználó vagy hibás jelszó!")
    Menu()


def Regisztracio():
    username = input("Adj meg egy felhasználó nevet: ")
    with open('felhasznalok.txt', 'r') as file:
        ellenorzes = file.readlines()
        for sor in ellenorzes:
            adatok = sor.strip().split(';')
            if adatok[1] == username:
                print("Ez a felhasználó név már létezik!")
                return
        NewID = int(ellenorzes[-1].split(';')[0]) + 1 if ellenorzes else 1
    password = input("Add meg egy jelszót: ")
    with open('felhasznalok.txt', 'a') as file:
        file.write(f"{NewID};{username};{password}\n")
    os.makedirs(f"users/{username}", exist_ok=True)
    with open(f"users/{username}/user_metadata.json", 'w') as meta_file:
        json.dump({}, meta_file)
    print("Sikeres regisztráció!")
    Menu()


def UserMenu(user):
    print(f"Üdv, {user.nev}!")  
    print("N: Új fájl létrehozása")
    print("W: Fájlok megtekintése/szerkesztése")
    print("S: Fájl státusz változtatása")
    print("L: Kijelentkezés")
    while True:
        try:
            if keyboard.is_pressed('N'):
                UjFile(user)
            elif keyboard.is_pressed('W'):
                FajlSzerkVMegt(user)
                time.sleep(0.5)
            elif keyboard.is_pressed('S'):
                StatusValtMenu(user)
            elif keyboard.is_pressed('L'):
                print("Kijelentkezés...")
                Menu()
                break
        except:
            pass


def UjFile(user):
    user_mappa = f"users/{user.nev}"
    file_nev = input("Adj meg egy fájlnevet: ") + ".txt"
    file_path = os.path.join(user_mappa, file_nev)

    szoveg = input("Írd be a fájl tartalmát: ")
    with open(file_path, 'w') as file:
        file.write(szoveg)

    metadata_path = os.path.join(user_mappa, "user_metadata.json")
    with open(metadata_path, 'r') as meta_file:
        metadata = json.load(meta_file)

    metadata[file_nev] = {"done": False}
    with open(metadata_path, 'w') as meta_file:
        json.dump(metadata, meta_file)

    print(f"Fájl '{file_nev}' sikeresen létrehozva!")
    UserMenu(user)

def FajlSzerkVMegt(user):
    print("\n")
    print("W: Fájlok megtekintése")
    print("E: Fájlok szerkesztése")
    print("M: Vissza a főmenübe")
    while True:
        try:
            if keyboard.is_pressed('E'):
                FileSzerkesztes(user)
                time.sleep(0.5)

            elif keyboard.is_pressed('W'):
                FileMegtekintes(user)
                time.sleep(0.5)

            elif keyboard.is_pressed('M'):
                print("Vissza a főmenübe...")
                time.sleep(0.5)
                UserMenu(user)
                break
        except:
            pass


def FileMegtekintes(user):
    user_mappa = f"users/{user.nev}"
    metadata_path = os.path.join(user_mappa, "user_metadata.json")

    with open(metadata_path, 'r') as meta_file:
        metadata = json.load(meta_file)

    if metadata:
        print("Fájlok:")
        for file_nev, info in metadata.items():
            status = "Kész" if info["done"] else "Folyamatban"
            print(f"- {file_nev} [{status}]")

        file_nev = input("Add meg a fájl nevét, amit meg szeretnél nyitni: ") + ".txt"
        
        if file_nev in metadata:
            file_path = os.path.join(user_mappa, file_nev)
            try:
                with open(file_path, 'r') as file:
                    szoveg = file.read()
                    print(f"Tartalom a(z) {file_nev} fájlból:\n")
                    print(szoveg)
            except FileNotFoundError:
                print(f"Hiba: a fájl {file_nev} nem található.")
        else:
            print("Nem található ilyen fájl a fájlok listájában.")
        print("M: Vissza a főmenübe")
        print("E: Fájlok szerkesztése")
        while True:
            try:
                if keyboard.is_pressed('E'):
                    FileSzerkesztes(user)
                    time.sleep(0.5)

                elif keyboard.is_pressed('M'):
                    print("Vissza a főmenübe...")
                    time.sleep(0.5)
                    UserMenu(user)
                    break
            except:
                pass
    else:
        print("Nincsenek fájljaid.")

def FileSzerkesztes(user):
    user_mappa = f"users/{user.nev}"
    file_nev = input("Add meg a fájl nevét, amit szerkeszteni szeretnél: ") + ".txt"
    file_path = os.path.join(user_mappa, file_nev)

    try:
        with open(file_path, 'r') as file:
            tartalom = file.read()
            print(f"Jelenlegi tartalom a(z) {file_nev} fájlban:\n")
            print(tartalom)
    except FileNotFoundError:
        print(f"Hiba: a fájl {file_nev} nem található.")
        return

    print("Válassz az alábbi lehetőségek közül:")
    print("E: Fájl tartalmának szerkesztése")
    print("D: Fájl törlése")
    print("M: Vissza a főmenübe")    
    while True:
        try:
            if keyboard.is_pressed('E'):
                print("Add meg az új tartalmat:")
                with open(file_path, 'r') as file:
                    jel_taralom = file.read()
                    print(jel_taralom)
                uj_tartalom = input()
                with open(file_path, 'w') as file:
                    file.write(jel_taralom + uj_tartalom)
                print(f"A(z) {file_nev} fájl sikeresen frissítve!")
                UserMenu(user)
                break
            elif keyboard.is_pressed('D'):
                os.remove(file_path)
                metadata_path = os.path.join(user_mappa, "user_metadata.json")
                with open(metadata_path, 'r') as meta_file:
                    metadata = json.load(meta_file)
                if file_nev in metadata:
                    del metadata[file_nev]
                    with open(metadata_path, 'w') as meta_file:
                        json.dump(metadata, meta_file)
                print(f"A(z) {file_nev} fájl sikeresen törölve!")
                UserMenu(user)
                break
            elif keyboard.is_pressed('M'):
                print("Vissza a főmenübe...")
                time.sleep(0.5)
                UserMenu(user)
                break
        except:
            pass
    
def StatusValtMenu(user):
    print("\n")
    print("M: Vissza a főmenübe")
    print("F: Fájlok folyamatba váltása")
    print("D: Fájlok megjelölése készként")
    while True:
        try:
            if keyboard.is_pressed('M'):
                print("Vissza a főmenübe...")
                time.sleep(0.5)
                UserMenu(user)
                break
            elif keyboard.is_pressed('F'):
                time.sleep(0.5)
                Folyamatba(user)
                break
            elif keyboard.is_pressed('D'):
                time.sleep(0.5)
                MegjelolesKeszkent(user)
                break
        except:
            pass

def MegjelolesKeszkent(user):
    user_mappa = f"users/{user.nev}"
    metadata_path = os.path.join(user_mappa, "user_metadata.json")

    with open(metadata_path, 'r') as meta_file:
        metadata = json.load(meta_file)

    print("Fájlok:")
    for file_nev, info in metadata.items():
        status = "Kész" if info["done"] else "Folyamatban"
        print(f"- {file_nev} [{status}]")

    file_nev = input("Add meg a fájl nevét, amit készként szeretnél megjelölni: ") + ".txt"
    if file_nev in metadata:
        metadata[file_nev]["done"] = True
        with open(metadata_path, 'w') as meta_file:
            json.dump(metadata, meta_file)
        print(f"A '{file_nev}' fájl készként lett megjelölve!")
        UserMenu(user)
    else:
        print("Nem található ilyen fájl.")
        StatusValtMenu(user)

def Folyamatba(user):
    user_mappa = f"users/{user.nev}"
    metadata_path = os.path.join(user_mappa, "user_metadata.json")

    with open(metadata_path, 'r') as meta_file:
        metadata = json.load(meta_file)

    print("Fájlok:")
    for file_nev, info in metadata.items():
        status = "Kész" if info["done"] else "Folyamatban"
        print(f"- {file_nev} [{status}]")

    file_nev = input("Add meg a fájl nevét, amit folyamatba szeretnél váltani: ") + ".txt"
    if file_nev in metadata:
        metadata[file_nev]["done"] = False
        with open(metadata_path, 'w') as meta_file:
            json.dump(metadata, meta_file)
        print(f"A '{file_nev}' fájl folyamatba állítva!")
        UserMenu(user)
    else:
        print("Nem található ilyen fájl.")
        StatusValtMenu(user)

print("start")
Menu()