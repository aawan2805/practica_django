import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')

import django
django.setup()

from biblioteca_barcelona.models import *
from faker import Faker
from datetime import date

fake = Faker('es_ES')

# numbers = set(fake.unique.random_int() for i in range(1000))

from random import randint

POSSIBLE_LETTERS = (
    "T",
    "R",
    "W",
    "A",
    "G",
    "M",
    "Y",
    "F",
    "P",
    "D",
    "X",
    "B",
    "N",
    "J",
    "Z",
    "S",
    "Q",
    "V",
    "H",
    "L",
    "C",
    "K",
    "E",
    "T",
)

# Insert de les biblioteques
biblioteques = [] # Tindrem el control de les bibliotques afegides. No haurem de fer queries per a obtenir-les.
while len(biblioteques) < 50: # No sortim fins a tenir 50 biblioteques inserides
    codi_biblioteca = fake.unique.random_number(digits=10)
    nom = fake.unique.city()
    try:
        pass
        bib = Biblioteca(codi=codi_biblioteca, nom=nom)
        bib.save()
        biblioteques.append(bib)
    except:
        pass
print("Biblioteques inserides.")


# Insert dels codis postals
cps = []
i = 0
while len(cps) != len(biblioteques): # No sortim fins a tenir 50 codis postals. Ja que cada biblioteca se li associa una codi postal.
    # Try per a la restricció de la clau primaria.
    try:
        codi_postal = fake.unique.postcode()
        bib = biblioteques[i] # Per a cada biblioteca li associem un codi postal random.
        cp = CodiPostal(codi=codi_postal, biblioteca=bib)
        cp.save()
        cps.append(cp)
        i += 1
    except:
        pass
print("Codis postals inserits.")


# Insert dels horaris
dies = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"] # Dies permesos
hora_obertura = ["08", "09", "10"]
hora_tancament = ["14", "20", "22"]

for biblioteca in biblioteques: # Per a cada biblioteca tindrem horaris
    for i in range(7): # 7 horaris per a cada biblioteca
        obertura = fake.random_choices(elements=hora_obertura, length=1)[0] # Obtenim una hora d'obertura random
        tancament = fake.random_choices(elements=hora_tancament, length=1)[0] # Obtenim una hora de tancament random
        Horari(dia=dies[i], hora_obertura=obertura, hora_tancament=tancament, biblioteca=biblioteca).save() # Inserim els 7 díes de la setmana
print("7 horaris inserits per a cada biblioteca.")


# Insert dels socis
socios = []
for i in range(1000):
    numero_dni = randint(10000000, 99999999)
    letra_dni = POSSIBLE_LETTERS[numero_dni % 23]

    dni = f"{numero_dni}{letra_dni}"
    nom = fake.first_name()
    cognom = fake.last_name()
    data_naixement = fake.date_between(start_date="-60y") # Data d'aqui a 60 anys enrere.

    # Obtenim una biblioteca qualsevol per a poder associar-la al soci.
    rand_bib = fake.random_number(digits=10) % len(biblioteques)
    bib = biblioteques[rand_bib]

    try:
        sc = Soci(dni=dni, nom=nom, cognom=cognom, data_naixement=data_naixement, biblioteca=bib)
        sc.save()
        socios.append(sc)
    except:
        pass
print("Socis inserits.")


# Insert de concursos
concursos_inserits = 0
while concursos_inserits < 20:
    rand_bib_1 = fake.random_number(digits=10) % len(biblioteques)
    rand_bib_2 = fake.random_number(digits=10) % len(biblioteques)

    biblioteca1 = biblioteques[rand_bib_1]
    biblioteca2 = biblioteques[rand_bib_2]

    if biblioteca1 != biblioteca2: # RS: dues biblioteques no poden ser les mateixes
        dt = fake.unique.date_between() # Obtenim una data qualsevol. D'aqui a 30 anys.
        edat_minima = fake.unique.random_int(min=10, max=40)
        concurs = Concurs(data=dt, edat_minima=edat_minima, biblioteca1=biblioteca1, biblioteca2=biblioteca2)
        concurs.save()

        num_socis_concurs = fake.random_int(min=1, max=10)
        for i in range(num_socis_concurs):
            rand_socis = fake.random_number(digits=10) % len(socios) # Obteim qualsevol soci random
            s = socios[rand_socis]
            if (concurs.data.year - s.data_naixement.year) >= concurs.edat_minima: # Mirem la RS d'edat per a l'assitencia al concurs
                concurs.socis.add(s) # Afegim el soci al N-N entre Soci i Biblioteca
        concursos_inserits += 1
print("Concursos inserits.")


materials = []
llibres = []
accesoris = []
while len(materials) != 1000:
    try:
        if len(materials) <= 500: # inserim els llibres. Fem aquest control pels llibres.
            isbn = fake.unique.isbn13(separator="")
        else: # Accesorias amb el ean13
            isbn = fake.unique.ean13()

        nom = fake.catch_phrase()
        mat = Material(codi_barres=isbn, nom=nom)
        mat.save()
        materials.append(mat)
    except:
        pass

print("Materials inserits.")


for i in range(500):
    # Els 500 primers materials serán llibres
    autor = fake.name()
    mt = materials[i]

    llb = Llibre(autor=autor, codi_barres_material=mt)
    llb.save()
print("Llibres creats.")


for i in range(500,1000):
    # Els 500 últims materials serán accesoris
    mt = materials[i]
    tipus = fake.name()

    acc = Accesori(tipus=tipus, codi_barres_accesori=mt)
    acc.save()
print("Accesoris creats.")


quantitzacions = []
for i in range(1):
    # Creem la taula associativa quantització
    for i, bib in enumerate(biblioteques): # Deixem alguns materials per la cardinalitat de 0..* - 0..* de Biblioteca a Material
        if i % 5 == 0:
            continue

        n_materials = fake.random_int(min=0, max=len(materials)) # Assigname N materials
        for _ in range(n_materials):
            m = fake.random_int(min=10, max=len(materials)) % len(materials)
            material = materials[m]

            numero_mostres = fake.random_int(min=1, max=15)

            try:
                quant = Quantitzacio(material=material, biblioteca=bib, quantitat=numero_mostres)
                quant.save()
                quantitzacions.append({
                    'biblioteca': bib,
                    'material': material,
                })
            except:
                pass

    for i, material in enumerate(materials):
        if i % 5 == 0: # poden haber materials que no estiguin en cap bibliotec
            continue

        n_biblioteca = fake.random_int(min=0, max=len(biblioteques))
        for _ in range(n_biblioteca):
            b = fake.random_int(min=10, max=len(biblioteques)) % len(biblioteques)
            biblio = biblioteques[b]

            numero_mostres = fake.random_int(min=1, max=20)

            try:
                quant = Quantitzacio(material=material, biblioteca=biblio, quantitat=numero_mostres)
                quant.save()
                quantitzacions.append({
                    'biblioteca': bib,
                    'material': material,
                })
            except:
                pass
# dni =
