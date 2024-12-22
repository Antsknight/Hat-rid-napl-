import keyboard

class Felhasznalo:
    def __init__(self,id,nev,jelszo):
        self.id = id
        self.nev = nev
        self.jelszo = jelszo


def Menu():
    asd = True
    print("Bejelentkezéshez nyomd meg a ,b, regisztrációhoz az ,r, betűt! ")
    while asd:
        try:  
            if keyboard.is_pressed('b'):  
               asd = False
               return Bejelentkezes()
            elif keyboard.is_pressed('r'):
               asd = False
            
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


print("start")
felhasznalo = Menu()
print(felhasznalo.nev)
