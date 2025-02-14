"""name = 'Meier'
my_name = 'Linus'
age = '17'
city ='Freiburg'
its_woman = True
if its_woman:
    print('Sehr geehrte Frau '+ name)
else:
    print('Sehr geehrter Herr '+name)

print('Mein Name ist '+ my_name)
print('ich bin bald '+age+' Jahre alt')
print('und ich komme aus '+ city)

x = 10
y = 3.14
name = "Alice"
is_active = True

# Datentypen überprüfen
print(type(x))  # <class 'int'>
print(type(y))  # <class 'float'>
print(type(name))  # <class 'str'>
print(type(is_active))  # <class 'bool'>

fruits = ["apple", "banana", "cherry"]

# Element hinzufügen
fruits.append("orange")

# Element entfernen
fruits.remove("banana")

# Zugriff auf Elemente
print(fruits[-3])  # "apple"
print(fruits[2])  # "orange"

eingabe = input("Gib deinen Namen ein: ")
print("Hallo, " + eingabe + "!")

for i in range(5):
    print(i)  # Gibt 0 bis 4 aus

x = 0
while x < 5:
    print(x)
    x += 1

def sag_hallo(name):
    return "Hallo, " + name

print(sag_hallo("Max"))

while True:
    try:
        zahl = int(input("Gib eine Zahl ein: "))
        print(10 / zahl)
    except ZeroDivisionError:
        print("Fehler: Division durch 0 ist nicht erlaubt.")
    except ValueError:
        print("Fehler: Bitte eine gültige Zahl eingeben.")

person = {"name": "Alice", "alter": 25, "stadt": "Berlin"}
print(person["name"])  # Gibt "Alice" aus
person["beruf"] = "Entwickler"  # Fügt ein neues Schlüssel-Wert-Paar hinzu

koordinaten = (10, 20)
print(koordinaten[0])  # Gibt 10 aus

zahlen_set = {1, 2, 3, 4, 5}
zahlen_set.add(6)  # Fügt 6 zum Set hinzu
print(3 in zahlen_set) # Prüft, ob 3 im Set enthalten ist (True)

quadrate = [x**2 for x in range(5)]
quadrate.remove(4)
print(quadrate)  # Gibt [0, 1, 4, 9, 16] aus

class Person:
    def __init__(self, name, alter):
        self.name = name
        self.alter = alter

    def vorstellen(self):
        print(f"Hallo, ich heiße {self.name} und bin {self.alter} Jahre alt.")



p1 = Person("Max", 30)
p1.vorstellen()  # Gibt "Hallo, ich heiße Max und bin 30 Jahre alt." aus
quadrat = lambda x: x ** 4
print(quadrat(5))  # Gibt 25 aus

# Datei schreiben
with open("datei.txt", "w") as file:
    file.write("Hallo, Welt!")

# Datei lesen
with open("datei.txt", "r") as file:
    inhalt = file.read()
    print(inhalt)


import math
print(math.sqrt(16))  # Gibt 4.0 aus

def ln(x):
    return math.log(x,math.e)

print(ln(2))


def ableitung(x, c, a):
    a2 = a*c
    c2 = c - 1
    fx = a2*x**c2
    return fx
print(ableitung(4,2,7))"""

fruechte = ["Apfel", "Banane", "Kirsche"]
for index, frucht in enumerate(fruechte):
    print(f"{index}: {frucht}")