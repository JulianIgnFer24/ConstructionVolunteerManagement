# Llamar a crear_equipo_construccion(cantidad_casas), donde cantidad_casas es un entero positivo que representa la cantidad de casas a construir.
# El resultado será una lista de listas, donde la primera lista contiene los monitores, la segunda lista contiene los jefes de escuela y las siguientes 
# listas contienen los voluntarios de cada cuadrilla.

# este algoritmo es usando el algoritmo de "greedy" para balancear las cuadrillas, es decir que la suma de los valores de las habilidades de los voluntarios 
# sea lo más balanceada posible entre todas las cuadrillas.


from neo4j import GraphDatabase
import math

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(user, password))

def obtener_voluntarios():
    with driver.session() as session:
        result = session.run("""
            MATCH (v:Voluntario)-[r1:TIENE_HABILIDAD]->(c1:Caracteristica {tipo: "Constructiva"})
            MATCH (v)-[r2:TIENE_HABILIDAD]->(c2:Caracteristica {tipo: "Social"})
            MATCH (v)-[r3:TIENE_HABILIDAD]->(c3:Caracteristica {tipo: "PerspectivaGenero"})
            RETURN 
                v.dni AS DNI,
                r1.valor AS Constructiva,
                r2.valor AS Social,
                r3.valor AS Genero
        """)
        
        return [record.data() for record in result]

# voluntarios = obtener_voluntarios()
# print(voluntarios)


def obtener_monitores(n):
    with driver.session() as session:
        result = session.run("""
            MATCH (v:Voluntario)-[r1:TIENE_HABILIDAD]->(:Caracteristica {tipo: "Constructiva"})
            MATCH (v)-[r2:TIENE_HABILIDAD]->(:Caracteristica {tipo: "Social"})
            WHERE r1.valor = 10 AND r2.valor >= 8
            RETURN v.dni AS DNI, r2.valor AS Social
            ORDER BY r2.valor DESC
        """)
        # Limitar el número de monitores a los primeros 'n' después de ordenar
        return [record["DNI"] for record in result][:n]



# voluntarios = obtener_monitores(5)

# print("Voluntarios filtrados por habilidades altas (Constructiva y Social ≥ 8):\n")
# print(voluntarios)


def obtener_jefes_escuela(n):
    # Primero, obtenemos los monitores (suponiendo que la función obtener_dnis_monitores ya está definida)
    monitores = obtener_monitores(n)
    
    with driver.session() as session:
        result = session.run("""
            MATCH (v:Voluntario)-[r2:TIENE_HABILIDAD]->(:Caracteristica {tipo: "Social"})
            MATCH (v)-[r3:TIENE_HABILIDAD]->(:Caracteristica {tipo: "PerspectivaGenero"})
            WHERE r2.valor = 10 AND r3.valor >= 8
            RETURN v.dni AS DNI, r3.valor AS Genero
            ORDER BY r3.valor DESC
        """)
        
        jefes_validos = []
        
        # Filtramos para que los jefes no sean monitores
        for record in result:
            dni = record["DNI"]
            if dni not in monitores:
                jefes_validos.append(dni)
            
            # Limitar a los primeros n jefes válidos
            if len(jefes_validos) == n:
                break
        
        return jefes_validos

    
# escuela = obtener_jefes_escuela(5)
# print("Jefes de Escuela filtrados por habilidades altas (Social y Género ≥ 8):\n")
# print(escuela)


import math

def crear_cuadrillas_balanceadas(cantidad_casas):
    # 1) Obtener y excluir monitores/jefes (listas de DNIs)
    cantidad_monitores = math.ceil(cantidad_casas / 7)
    monitores = obtener_monitores(cantidad_monitores)
    jefes = obtener_jefes_escuela(cantidad_monitores)
    dnis_excluir = set(monitores + jefes)

    # 2) Filtrar voluntarios disponibles
    todos = obtener_voluntarios()
    voluntarios_disponibles = [
        v for v in todos if v['DNI'] not in dnis_excluir
    ]

    # 3) Calcular total de habilidades y ordenar ascendente
    for v in voluntarios_disponibles:
        v['TotalHabilidad'] = v['Constructiva'] + v['Social'] + v['Genero']
    voluntarios_ordenados = sorted(
        voluntarios_disponibles, key=lambda x: x['TotalHabilidad']
    )

    # 4) Definir tamaños de cuadrilla más balanceados
    total = len(voluntarios_ordenados)
    base = total // cantidad_casas
    extra = total % cantidad_casas
    tamaños = [
        base + 1 if i < extra else base
        for i in range(cantidad_casas)
    ]

    # 5) Inicializar cuadrillas vacías y punteros
    cuadrillas = [[] for _ in range(cantidad_casas)]
    i, j, idx = 0, total - 1, 0

    # 6) Reparto “greedy” de extremos
    while i <= j:
        if len(cuadrillas[idx]) < tamaños[idx]:
            cuadrillas[idx].append(voluntarios_ordenados[i])
            i += 1
        if i <= j and len(cuadrillas[idx]) < tamaños[idx]:
            cuadrillas[idx].append(voluntarios_ordenados[j])
            j -= 1
        idx = (idx + 1) % cantidad_casas

    # 7) Ordenar cada cuadrilla internamente por TotalHabilidad descendente
    cuadrillas_ordenadas = []
    for grupo in cuadrillas:
        grupo_ordenado = sorted(grupo, key=lambda x: x['TotalHabilidad'], reverse=True)
        cuadrillas_ordenadas.append([v['DNI'] for v in grupo_ordenado])

    return cuadrillas_ordenadas



cuadrillas = crear_cuadrillas_balanceadas(100)  # ejemplo: 10 casas
for num, cuadro in enumerate(cuadrillas, start=1):
    print(f"Cuadrilla {num}:")
    for dni in cuadro:
        print(f"  - {dni}")
    print()
    
    

def crear_equipo_construccion(cantidad_casas):
    cant_monitores = math.ceil(cantidad_casas / 7)  # Cantidad de monitores necesarios
    monitores = obtener_monitores(cant_monitores)  # Obtener monitores necesarios
    jefes = obtener_jefes_escuela(cant_monitores)  # Obtener jefes de escuela necesarios
    cuadrillas = crear_cuadrillas_balanceadas(cantidad_casas)  # Crear cuadrillas balanceadas
    return( [monitores] + [jefes] + [cuadrillas[i] for i in range(len(cuadrillas))])

# print("Equipo de construcción:")
# print(crear_equipo_construccion(100))  # ejemplo: 10 casas
# print("MONITORES: ")
# print(obtener_monitores(math.ceil(100 / 7)))


# las funciones tienen que devolver una lista  de Dni donde el primero sea el jefe de cuadrilla y el resto voluntarios 

