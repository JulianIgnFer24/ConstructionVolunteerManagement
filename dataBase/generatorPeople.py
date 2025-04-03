import pandas as pd
import random
from faker import Faker

fake = Faker("es_ES")

provincias = ["Buenos Aires", "Córdoba", "Santa Fe", "Tucumán", "Salta", "Entre Ríos", "Misiones",
              "Corrientes", "San Juan", "San Luis", "La Pampa", "Neuquén", "Río Negro", "Chubut",
              "Santa Cruz", "Tierra del Fuego", "Jujuy", "Santiago del Estero", "Catamarca", "La Rioja",
              "Chaco", "Formosa"]

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

    # Mayor experiencia en habilidades para mayores de 25
    if edad < 25:
        habilidad_constructiva = random.randint(1, 7)
        habilidad_social = random.randint(1, 7)
        habilidad_perspectiva_genero = random.randint(1, 7)
    else:
        habilidad_constructiva = random.randint(5, 10)
        habilidad_social = random.randint(5, 10)
        habilidad_perspectiva_genero = random.randint(5, 10)

    # 95% de las personas son de Mendoza
    provincia = "Mendoza" if random.random() < 0.95 else random.choice(provincias)

    data.append([
        nombre, apellido, edad, genero, provincia,
        habilidad_constructiva, habilidad_social,
        habilidad_perspectiva_genero
    ])

df = pd.DataFrame(data, columns=[
    "Nombre", "Apellido", "Edad", "Género", "Provincia",
    "Habilidad Constructiva", "Habilidad Social",
    "Habilidad de Perspectiva de Género"
])

df.to_excel("ConstructionVolunteerManagement/dataBase/voluntarios.xlsx", index=False, engine="openpyxl")

print("Archivo 'voluntarios.xlsx' creado con éxito.")
