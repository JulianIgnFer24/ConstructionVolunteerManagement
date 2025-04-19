import pandas as pd

# Cargar el CSV original
df = pd.read_csv('voluntariosCSV2.csv')

# Asegurar que haya una columna de identificador
if 'nodeid' not in df.columns:
    df['nodeid'] = df.index  # Usa el índice como nodeid si no existe

# Mapear columnas originales a tipo de habilidad
columnas_a_exportar = {
    "Habilidad Social": "Social",
    "Habilidad Constructiva": "Constructiva",
    "Habilidad de Perspectiva de Género": "PerspectivaGenero"
}

# Crear un CSV por cada tipo de habilidad
for columna, tipo in columnas_a_exportar.items():
    df_salida = pd.DataFrame({
        "nodeid": df['nodeid'],
        "tipo": tipo,
        "valor": df[columna]
    })
    nombre_archivo = f"habilidades_{tipo}.csv"
    df_salida.to_csv(nombre_archivo, index=False)
    print(f"✅ Archivo generado: {nombre_archivo}")
