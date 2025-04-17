from flask import Flask, render_template, request
from neo4j import GraphDatabase
import query_cuadrillas

app = Flask(__name__)

# Conexión a Neo4j
uri = "bolt://localhost:7687"
user = "neo4j"
password = "testing123"
driver = GraphDatabase.driver(uri, auth=(user, password))

def obtener_voluntarios_total():
    """Obtiene todos los voluntarios de la base de datos."""
    with driver.session() as session:
        result = session.run("""
            MATCH (v:Voluntario)
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})
            RETURN v.nombre AS Nombre, v.apellido AS Apellido, v.dni AS DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """)
        return [record.data() for record in result]

def obtener_datos_voluntario(dni):
    with driver.session() as session:
        result = session.run("""
            MATCH (v:Voluntario {dni: $dni})
            optional MATCH (v)-[h1:TIENE_HABILIDAD]->(ha1:Caracteristica {tipo: 'Constructiva'})
            optional MATCH (v)-[h2:TIENE_HABILIDAD]->(ha2:Caracteristica {tipo: 'Social'})
            optional MATCH (v)-[h3:TIENE_HABILIDAD]->(ha3:Caracteristica {tipo: 'PerspectivaGenero'})
            RETURN 
                v.nombre AS Nombre, 
                v.apellido AS Apellido, 
                v.dni AS DNI, 
                h1.valor AS Constructivo, 
                h2.valor AS Social, 
                h3.valor AS PerspectivaGenero
        """, dni=dni).single()
        return result.data() if result else {}

def armar_cuad(casas):
    cuadrillas = query_cuadrillas.crear_equipo_construccion(casas)

    monitores = [obtener_datos_voluntario(dni) for dni in cuadrillas[0]]
    jefes_escuela = [obtener_datos_voluntario(dni) for dni in cuadrillas[1]]

    cuadrillas_completas = []
    for i in range(2, len(cuadrillas)):
        cuadrilla = [obtener_datos_voluntario(dni) for dni in cuadrillas[i]]
        cuadrillas_completas.append(cuadrilla)

    return monitores, jefes_escuela, cuadrillas_completas



def voluntarios_potenciar():
    """Consulta para obtener los voluntarios que pueden potenciar."""
    with driver.session() as session:
        result = session.run("""
            MATCH (v:Voluntario)-[:PARTICIPO_EN]->(e)
            match (v:Voluntario) -[h1:TIENE_HABILIDAD]-> (r1{tipo:"Constructiva"})
            match (v:Voluntario) -[h2:TIENE_HABILIDAD]-> (r2{tipo:"Social"})
            match (v:Voluntario) -[h3:TIENE_HABILIDAD]-> (r3{tipo:"PerspectivaGenero"})
            WITH v, COUNT(e) AS cantidadEventos, h1.valor as constructivo, h2.valor as social, h3.valor as genero
            WHERE cantidadEventos = 1 and (constructivo + social + genero) >= 24
            RETURN v.nombre AS Nombre, v.apellido as Apellido, v.dni as DNI, constructivo as Constructivo, social as Social, genero as PerspectivaGenero
        """)
        return [record.data() for record in result]

def candidatos_monitor():
    """Consulta para obtener los candidatos a monitor."""
    with driver.session() as session:
        result = session.run("""
            match (v:Voluntario) -[r1:TIENE_HABILIDAD]-> (c:Caracteristica{tipo:"Constructiva"})
            match (v:Voluntario) -[r2:TIENE_HABILIDAD]-> (s:Caracteristica{tipo:"Social"})
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})
            where r1.valor =10 and r2.valor >= 8
            return v.nombre as Nombre, v.apellido as Apellido, v.dni as DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """)
        return [record.data() for record in result]

def candidatos_jefe_cuadrilla():
    """Consulta para obtener los candidatos a jefe de cuadrilla."""
    with driver.session() as session:
        result = session.run("""
            match (v:Voluntario) -[r1:TIENE_HABILIDAD]-> (c:Caracteristica{tipo:"Constructiva"})
            match (v:Voluntario) -[r2:TIENE_HABILIDAD]-> (s:Caracteristica{tipo:"Social"})
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})

            where r1.valor >= 8 and r2.valor >= 8
            return v.nombre as Nombre, v.apellido as Apellido, v.dni as DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """)
        return [record.data() for record in result]

def candidatos_jefe_escuela():
    """Consulta para obtener los candidatos a jefe de escuela."""
    with driver.session() as session:
        result = session.run("""
            match (v:Voluntario) -[r1:TIENE_HABILIDAD]-> (c:Caracteristica{tipo:"PerspectivaGenero"})
            match (v:Voluntario) -[r2:TIENE_HABILIDAD]-> (s:Caracteristica{tipo:"Social"})
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})

            where r1.valor >= 8 and r2.valor = 10
            return v.nombre as Nombre, v.apellido as Apellido, v.dni as DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """)
        return [record.data() for record in result]


@app.route('/')
def index():
    """Página principal que muestra la lista de voluntarios."""
    voluntarios = obtener_voluntarios_total()
    return render_template('index.html', voluntarios=voluntarios, titulo = "Lista de Voluntarios")

@app.route('/armar-cuadrillas', methods=['POST'])
def armar_cuadrillas():
    casas = int(request.form['numero_casas'])
    monitores, jefes_escuela, cuadrillas = armar_cuad(casas)

    return render_template(
        'index.html',
        monitores=monitores,
        jefes_escuela=jefes_escuela,
        cuadrillas=cuadrillas,
        titulo="Cuadrillas Armadas"
    )


@app.route('/perfiles-potenciar')
def perfiles_potenciar():
    voluntarios = voluntarios_potenciar()
    return render_template('index.html', voluntarios=voluntarios, titulo = "Voluntarios a Potenciar")

@app.route('/buscar-candidatos')
def buscar_candidatos():
    tipo = request.args.get('tipo')  # obtiene el valor seleccionado

    if tipo == 'monitor':
        voluntarios = candidatos_monitor()
        tipo_candidato = "Monitor"
    elif tipo == 'jefe_cuadrilla':
        voluntarios = candidatos_jefe_cuadrilla()
        tipo_candidato = "Jefe de Cuadrilla"
    elif tipo == 'jefe_escuela':
        voluntarios = candidatos_jefe_escuela()
        tipo_candidato = "Jefe de Escuela"
    else:
        voluntarios = []
        tipo_candidato = "Desconocido"
    return render_template('index.html', voluntarios=voluntarios, titulo = f"Candidatos a {tipo_candidato}")

@app.route('/buscar-por-atributo', methods=['GET'])
def buscar_por_atributo():
    atributo = request.args.get('atributo')
    valor = request.args.get('valor')

    if not atributo or not valor:
        return "Faltan datos", 400

    query = ""
    params = {'valor': valor}

    if atributo == "nombre":
        query = """
            MATCH (v:Voluntario)
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})
            WHERE toLower(v.nombre) CONTAINS toLower($valor)
            RETURN v.nombre AS Nombre, v.apellido AS Apellido, v.dni AS DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """
        atributo_final = "Nombre"

    elif atributo == "apellido":
        query = """
            MATCH (v:Voluntario)
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})
            WHERE toLower(v.apellido) CONTAINS toLower($valor)
            RETURN v.nombre AS Nombre, v.apellido AS Apellido, v.dni AS DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """
        atributo_final = "Apellido"

    elif atributo == "nombre_apellido":
        query = """
            MATCH (v:Voluntario)
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})
            WHERE toLower(v.nombre) CONTAINS toLower($valor) OR toLower(v.apellido) CONTAINS toLower($valor)
            RETURN v.nombre AS Nombre, v.apellido AS Apellido, v.dni AS DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """
        atributo_final = "Nombre o Apellido"

    elif atributo == "dni":
        query = """
            MATCH (v:Voluntario)
            match (v:Voluntario) -[ha1:TIENE_HABILIDAD]-> (re1{tipo:"Constructiva"})
            match (v:Voluntario) -[ha2:TIENE_HABILIDAD]-> (re2{tipo:"Social"})
            match (v:Voluntario) -[ha3:TIENE_HABILIDAD]-> (re3{tipo:"PerspectivaGenero"})
            WHERE v.dni = $valor
            RETURN v.nombre AS Nombre, v.apellido AS Apellido, v.dni AS DNI, ha1.valor as Constructivo, ha2.valor as Social, ha3.valor as PerspectivaGenero
        """
        atributo_final = "DNI"

    else:
        return "Atributo no válido", 400

    with driver.session() as session:
        result = session.run(query, params)
        voluntarios = [record.data() for record in result]

    return render_template('index.html', voluntarios=voluntarios, titulo = f"Lista de Voluntarios que contienen '{valor}' en '{atributo_final}'")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
