from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Funzione per connettersi al database MySQL
def connetti_db():
    return mysql.connector.connect(
        host="localhost",      # Cambia con l'host del tuo database
        user="root",           # Cambia con il tuo username
        password="",           # Cambia con la tua password
        database="Animali"     # Cambia con il nome del tuo database
    )

# Route per ottenere i dati in formato JSON
@app.route('/api/animali', methods=['GET'])
def get_animali():
    connessione = connetti_db()
    cursore = connessione.cursor(dictionary=True)
    cursore.execute("SELECT * FROM Mammiferi")
    animali = cursore.fetchall()
    cursore.close()
    connessione.close()
    return jsonify(animali)

@app.route('/api/animali', methods=['POST'])
def add_animali():
    data = request.get_json()
    if not all(key in data for key in ('Nome_Proprio', 'Razza', 'Peso', 'Eta')):
        return jsonify({"error": "Dati mancanti"}), 400

    nome = data['Nome_Proprio']
    razza = data['Razza']
    peso = data['Peso']
    eta = data['Eta']

    connessione = connetti_db()
    cursore = connessione.cursor()

    sql = "INSERT INTO Mammiferi (Nome_Proprio, Razza, Peso, Eta) VALUES (%s, %s, %s, %s)"
    cursore.execute(sql, (nome, razza, peso, eta))
    connessione.commit()

    cursore.close()
    connessione.close()

    return jsonify({"message": "Animale inserito con successo!"}), 201

@app.route('/api/animali/<int:id>', methods=['PUT'])
def update_mammifero(id):
    data = request.get_json()
    if not all(key in data for key in ('Nome_Proprio', 'Razza', 'Peso', 'Eta')):
        return jsonify({"error": "Dati mancanti"}), 400

    nome = data['Nome_Proprio']
    razza = data['Razza']
    peso = data['Peso']
    eta = data['Eta']

    connessione = connetti_db()
    cursore = connessione.cursor()

    sql = "UPDATE Mammiferi SET Nome_Proprio = %s, Razza = %s, Peso = %s, Eta = %s WHERE Id = %s"
    cursore.execute(sql, (nome, razza, peso, eta, id))
    connessione.commit()

    rowcount = cursore.rowcount
    cursore.close()
    connessione.close()

    if rowcount == 0:
        return jsonify({"message": "Animale non trovato"}), 404

    return jsonify({"message": "Animale aggiornato con successo!"}), 200

@app.route('/api/animali/<int:id>', methods=['DELETE'])
def delete_mammifero(id):
    connessione = connetti_db()
    cursore = connessione.cursor()

    cursore.execute("SELECT * FROM Mammiferi WHERE Id = %s", (id,))
    if not cursore.fetchone():
        cursore.close()
        connessione.close()
        return jsonify({"message": "Animale non trovato"}), 404

    cursore.execute("DELETE FROM Mammiferi WHERE Id = %s", (id,))
    connessione.commit()

    cursore.close()
    connessione.close()

    return jsonify({"message": "Animale eliminato con successo!"}), 200

if __name__ == '__main__':
    app.run(debug=True)