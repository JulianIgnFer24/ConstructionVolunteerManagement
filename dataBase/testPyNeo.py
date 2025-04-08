from neo4j import GraphDatabase

# Conectar con la base de datos
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "testing123"))

# Función que ejecuta la consulta y procesa los resultados
def obtener_voluntarios():
    with driver.session() as sesion:
        def ejecutar_consulta(tx):
            resultado = tx.run("MATCH (v:Voluntario) RETURN v.dni AS dni")
            return [registro["dni"] for registro in resultado]
        nombres_voluntarios = sesion.execute_read(ejecutar_consulta)
        for nombre in nombres_voluntarios:
            print(nombre)

# Llamar a la función
obtener_voluntarios()

# Cerrar el driver al finalizar
driver.close()
