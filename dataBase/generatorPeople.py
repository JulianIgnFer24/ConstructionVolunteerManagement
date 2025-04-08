import pandas as pd
import random
from faker import Faker
from datetime import datetime

fake = Faker("es_AR")
random.seed(42)
Faker.seed(42)

provincias = ["Buenos Aires", "Córdoba", "Santa Fe", "Tucumán", "Salta", "Entre Ríos", "Misiones",
              "Corrientes", "San Juan", "San Luis", "La Pampa", "Neuquén", "Río Negro", "Chubut",
              "Santa Cruz", "Tierra del Fuego", "Jujuy", "Santiago del Estero", "Catamarca", "La Rioja",
              "Chaco", "Formosa"]

construcciones = [
    ("Barrio Grilli Norte (Guaymallén)", "2021-04-05"),
    ("Barrio Grilli Sur (Guaymallén)", "2022-01-15"),
    ("Tierras Vivas (Lujan)", "2022-02-20"),
    ("Todos Unidos (Las Heras)", "2023-05-25"),
    ("Yañez (Maipu)", "2024-07-25"),
    ("Tierras Vivas (Lujan)", "2024-11-12"),
    ("Yañez (Maipu)", "2025-04-10")
]

data = []

for _ in range(500):
    genero = "Femenino" if random.random() < 0.6 else "Masculino"
    nombre = fake.first_name_female() if genero == "Femenino" else fake.first_name_male()
    apellido = fake.last_name()
    edad = random.randint(18, 29) if random.random() < 0.8 else random.randint(30, 60)

    hoy = datetime.now()
    año_nacimiento = hoy.year - edad
    fecha_nacimiento = fake.date_between_dates(
        date_start=datetime(año_nacimiento, 1, 1),
        date_end=datetime(año_nacimiento, 12, 31)
    )

    if edad < 25:
        habilidad_constructiva = random.randint(3, 7)
        habilidad_social = random.randint(1, 7)
        habilidad_perspectiva_genero = random.randint(1, 7)
    else:
        habilidad_constructiva = random.randint(5, 10)
        habilidad_social = random.randint(5, 10)
        habilidad_perspectiva_genero = random.randint(5, 10)

    provincia = "Mendoza" if random.random() < 0.95 else random.choice(provincias)

    max_possible = min(5, len(construcciones))
    num_construcciones = random.choices(
        [0, 1, 2, 3, 4, max_possible], 
        weights=[0.1, 0.3, 0.25, 0.2, 0.1, 0.05]
    )[0]
    
    construcciones_asistidas = random.sample(construcciones, num_construcciones) if num_construcciones > 0 else []

    if construcciones_asistidas:
        for barrio, fecha in construcciones_asistidas:
            data.append([
                nombre, apellido, edad, fecha_nacimiento, genero, provincia,
                habilidad_constructiva, habilidad_social, habilidad_perspectiva_genero,
                barrio, fecha
            ])
    else:
        data.append([
            nombre, apellido, edad, fecha_nacimiento, genero, provincia,
            habilidad_constructiva, habilidad_social, habilidad_perspectiva_genero,
            "Ninguna", ""
        ])

df = pd.DataFrame(data, columns=[
    "Nombre", "Apellido", "Edad", "Fecha Nacimiento", "Género", "Provincia",
    "Habilidad Constructiva", "Habilidad Social",
    "Habilidad de Perspectiva de Género", "Barrio", "Fecha"
])

df.to_excel("dataBase/voluntarios.xlsx", index=False, engine="openpyxl")

print("Archivo 'voluntarios.xlsx' creado con éxito.")
