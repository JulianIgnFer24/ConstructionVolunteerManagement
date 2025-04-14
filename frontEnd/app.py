from flask import Flask, render_template
from neo4j import GraphDatabase

app = Flask(__name__)

# Conexión a Neo4j
uri = "bolt://localhost:7687"
user = "neo4j"
password = "testing123"

driver = GraphDatabase.driver(uri, auth=(user, password))

def obtener_voluntarios():
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Voluntario)
            RETURN a.nombre AS Nombre, a.apellido AS Apellido, a.dni AS DNI
        """)
        return [record.data() for record in result]

@app.route('/')
def index():
    voluntarios = obtener_voluntarios()
    return render_template('index.html', voluntarios=voluntarios)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
