import mysql.connector

# Funzione per connettersi al database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Animali"
    )

# Dati degli animali da inserire
animali = [
    ("Bella", "Golden Retriever", 30, 5),
    ("Charlie", "Bulldog", 25, 4),
    ("Max", "Beagle", 15, 3),
    ("Lucy", "Chihuahua", 3, 2),
    ("Rocky", "Husky", 40, 6)
]

# Connessione al database e inserimento degli animali
mydb = connect_to_db()
mycursor = mydb.cursor()

sql = "INSERT INTO Mammiferi (Nome_Proprio, Razza, Peso, Eta) VALUES (%s, %s, %s, %s)"
mycursor.executemany(sql, animali)
mydb.commit()