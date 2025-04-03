import pandas as pd
import random
from faker import Faker
from datetime import datetime

fake = Faker("es_AR")

provincias = ["Buenos Aires", "Córdoba", "Santa Fe", "Tucumán", "Salta", "Entre Ríos", "Misiones",
              "Corrientes", "San Juan", "San Luis", "La Pampa", "Neuquén", "Río Negro", "Chubut",
              "Santa Cruz", "Tierra del Fuego", "Jujuy", "Santiago del Estero", "Catamarca", "La Rioja",
              "Chaco", "Formosa"]

construcciones = [
    ("Barrio Grilli Norte, Guaymallén", "2021-04-05"),
    ("Barrio Grilli Sur, Guaymallén", "2022-01-15"),
    ("Tierras Vivas, Lujan", "2022-02-20"),
    ("Todos Unidos, Las Heras", "2023-05-25"),
    ("Yañes, Maipu", "2024-07-25"),
    ("Tierras Vivas, Lujan", "2024-11-12"),
    ("Yañes, Maipu", "2025-04-10")
]

data = []

for _ in range(500):
    # 60% mujeres, 40% hombres
    genero = "Femenino" if random.random() < 0.6 else "Masculino"
    
    nombre = fake.first_name_female() if genero == "Femenino" else fake.first_name_male()
    apellido = fake.last_name()

    # 80% menores de 30
    if random.random() < 0.8:
        edad = random.randint(18, 29)
    else:
        edad = random.randint(30, 60)

    hoy = datetime.now()
    año_nacimiento = hoy.year - edad
    # Asegurarnos de que la fecha sea válida (no el 29 de febrero)
    fecha_nacimiento = fake.date_between_dates(
        date_start=datetime(año_nacimiento, 1, 1),
        date_end=datetime(año_nacimiento, 12, 31)
    )

    # Mayor experiencia en habilidades para mayores de 25
    if edad < 25:
        habilidad_constructiva = random.randint(3, 7)
        habilidad_social = random.randint(1, 7)
        habilidad_perspectiva_genero = random.randint(1, 7)
    else:
        habilidad_constructiva = random.randint(5, 10)
        habilidad_social = random.randint(5, 10)
        habilidad_perspectiva_genero = random.randint(5, 10)

    # 95% de las personas son de Mendoza
    provincia = "Mendoza" if random.random() < 0.95 else random.choice(provincias)

    # Generar lista de construcciones asistidas
    # Entre 0 y 5 construcciones, pero la mayoría habrá asistido a al menos 1max_possible = min(5, len(construcciones))  # No más de 5 ni más que construcciones disponibles
    max_possible = min(5, len(construcciones)) 

    num_construcciones = random.choices(
        [0, 1, 2, 3, 4, max_possible], 
        weights=[0.1, 0.3, 0.25, 0.2, 0.1, 0.05]
    )[0]
    
    construcciones_asistidas = random.sample(construcciones, num_construcciones) if num_construcciones > 0 else []
    
    # Formatear las construcciones asistidas como "Nombre (Fecha)"
    construcciones_formateadas = [f"{nombre} ({fecha})" for nombre, fecha in construcciones_asistidas]
    
    data.append([
        nombre, apellido, edad, fecha_nacimiento, genero, provincia,
        habilidad_constructiva, habilidad_social,
        habilidad_perspectiva_genero,
        ", ".join(construcciones_formateadas) if construcciones_formateadas else "Ninguna"
    ])

df = pd.DataFrame(data, columns=[
    "Nombre", "Apellido", "Edad", "Fecha Nacimiento", "Género", "Provincia",
    "Habilidad Constructiva", "Habilidad Social",
    "Habilidad de Perspectiva de Género", "Construcciones Asistidas"
])

df.to_excel("voluntarios.xlsx", index=False, engine="openpyxl")

print("Archivo 'voluntarios.xlsx' creado con éxito.")
