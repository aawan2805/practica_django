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
while len(biblioteques) < 15: # No sortim fins a tenir 50 biblioteques inserides
    codi_biblioteca = fake.unique.random_number(digits=10)
    nom = f'Biblioteca {fake.city()}'
    try:
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
for i in range(250):
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
while len(materials) != 150:
    try:
        if len(materials) <= 75: # inserim els llibres. Fem aquest control pels llibres.
            isbn = fake.unique.isbn13(separator="")
        else: # Accesorias amb el ean13
            isbn = fake.unique.ean13()

        nom = fake.catch_phrase()
        nom = nom[:45] if len(nom) >= 50 else nom

        mat = Material(codi_barres=isbn, nom=nom)
        mat.save()
        materials.append(mat)
    except:
        pass

print("Materials inserits.")


for i in range(75):
    # Els 500 primers materials serán llibres
    autor = fake.name()
    mt = materials[i]

    llb = Llibre(autor=autor, codi_barres_material=mt)
    llb.save()
print("Llibres creats.")


for i in range(75,150):
    # Els 500 últims materials serán accesoris
    mt = materials[i]
    tipus = fake.name()

    acc = Accesori(tipus=tipus, codi_barres_accesori=mt)
    acc.save()
print("Accesoris creats.")


quantitzacions = []
# Creem la taula associativa quantització
for i, bib in enumerate(biblioteques): # Deixem alguns materials per la cardinalitat de 0..* - 0..* de Biblioteca a Material
    if i % 5 == 0:
        continue

    n_materials = fake.random_int(min=1, max=len(materials)) # Assigname N materials
    for _ in range(n_materials):
        m = fake.random_int(min=1, max=len(materials)) % len(materials)
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

    n_biblioteca = fake.random_int(min=1, max=len(biblioteques))
    for _ in range(n_biblioteca):
        b = fake.random_int(min=1, max=len(biblioteques)) % len(biblioteques)
        biblio = biblioteques[b]

        quantitat_total = fake.random_int(min=1, max=20)

        try:
            quant = Quantitzacio(material=material, biblioteca=biblio, quantitat_total=quantitat_total, quantitat_disponible=quantitat_total)
            quant.save()
            quantitzacions.append({
                'biblioteca': bib,
                'material': material,
                'qt': numero_mostres
            })
        except:
            pass
print("Quantització afegit.")


from datetime import timedelta, date
prestecs = []
i = 0

# Primer afegim els prestecs que s'ha  retornat o no pero que no s'han demanat a altres biblioteques
while len(prestecs) <= 200:
    r_soci = fake.random_int(min=0, max=len(socios)-1) # Obtenim un soci qualsevol
    soci = socios[r_soci]

    biblioteca_del_soci = soci.biblioteca
    materials_bibliteca_soci = biblioteca_del_soci.materials.all()

    n_prestecs = fake.random_int(min=0, max=len(materials_bibliteca_soci)) % 7 # Posem 7 prestecs com a màxim
    for q in range(n_prestecs):
        qt_red = Quantitzacio.objects.get(biblioteca=biblioteca_del_soci, material=materials_bibliteca_soci[q])
        if qt_red.quantitat_disponible-1 < 0:
            break

        data_limit = fake.date_between(start_date=soci.data_naixement)

        if q % 2 == 0: # Posem de forma random que l'ha tornat.
            rand_days = fake.random_int(min=-15, max=15)
            data_retorn = data_limit + timedelta(days=rand_days) # Data de retorn + de 0 a 20 dies aleatoris
            while data_retorn > date.today(): # Ens assegurem que la data de retorn no sigui anterior a la data de naixement del soci :)
                 rand_days = fake.random_int(min=-5, max=5)
                 data_retorn = data_limit + timedelta(days=rand_days) # Data de retorn + de 0 a 20 dies aleatoris

        else: # No l'ha retornat encara
            data_retorn = None

        pr = Prestec(data_retorn=data_retorn, data_limit=data_limit, material=materials_bibliteca_soci[q], soci=soci)
        pr.save()
        prestecs.append(pr)

        # Reduïum la quantiat a la taula quantitzacio
        qt_red.quantitat_disponible = qt_red.quantitat_disponible-1
        qt_red.save()

while len(prestecs) <= 250: # Inserim 100 materials en prèstec pero demanats d'una altra biblioteca
    r_soci = fake.random_int(min=0, max=len(socios)-1) # Obtenim un soci qualsevol
    soci = socios[r_soci]

    biblioteca_del_soci = soci.biblioteca
    qt_material_soci = biblioteca_del_soci.quantitats.all().filter(quantitat_disponible=0) # Busquem els materials que están Out-Of-Stock

    if len(qt_material_soci) > 0:
        n_prestecs = fake.random_int(min=0, max=len(qt_material_soci))
        for q in range(n_prestecs):
            # Busquem totes les altres biblioteques que ho tinguin
            material_a_buscar = qt_material_soci[q].material
            qt_red = Quantitzacio.objects.filter(material=material_a_buscar, quantitat_disponible__gt=0)
            if len(qt_red) == 0: # Cap biblioteca ho té disponible.
                continue

            qt_red = qt_red[0]

            data_limit = fake.date_between(start_date=soci.data_naixement)
            data_estimacio = data_limit - timedelta(days=20)

            if q % 2 == 0: # Posem de forma random que l'ha tornat.
                rand_days = fake.random_int(min=-15, max=15)
                data_retorn = data_estimacio + timedelta(days=rand_days) # Data de retorn + de 0 a 20 dies aleatoris
                while data_retorn <= data_estimacio or data_retorn > date.today(): # Ens assegurem que la data de retorn no sigui anterior a la data de naixement del soci :)
                     rand_days = fake.random_int(min=-5, max=5)
                     data_retorn = data_limit + timedelta(days=rand_days) # Data de retorn + de 0 a 20 dies aleatoris

            else: # No l'ha retornat encara
                data_retorn = None

            pr = Prestec(data_retorn=data_retorn,
                         data_limit=data_limit,
                         material=qt_red.material,
                         soci=soci,
                         prestec_demanat=qt_red.biblioteca,
                         data_estimacio=data_estimacio)
            pr.save()
            prestecs.append(pr)

            # Reduïum la quantiat de la biblioteca on l'hem demanada a la taula quantitzacio
            qt_red.quantitat_disponible = qt_red.quantitat_disponible-1
            qt_red.save()


"""
203 | 1976-07-02  | 1976-07-20 | 1976-06-30     | 9780593104651 | 6616330997      | 85757528G

  id  | data_retorn | data_limit | data_estimacio |   material    | prestec_demanat |   soci
------+-------------+------------+----------------+---------------+-----------------+-----------
 1006 | 2010-11-09  | 2010-11-10 | 2010-10-21     | 9781554717415 | 6492101047      | 86439186B
  																			          (2553031124)
select * from prestec where material='9780593104651' and prestec_demanat='6616330997';
select * from prestec where material='9780593104651' and soci IN (SElECT soci.dni FROM soci JOIN biblioteca ON biblioteca.codi=soci.biblioteca WHERE biblioteca.codi='6616330997');
"""

"""
drop table auth_group cascade;
drop table auth_group_django_admin_log cascade;
drop table auth_permission cascade;
drop table auth_user_groups cascade;
drop table auth_user_user_permissions cascade;
drop table django_admin_log cascade;
drop table django_content_type cascade;
drop table django_migrations cascade;
drop table django_session cascade;
drop table auth_group_permissions cascade;
drop table auth_user cascade;
drop table django_migrations cascade;
drop table django_content_type cascade;

drop table biblioteca cascade;
drop table horari cascade;
drop table soci cascade;
drop table codipostal cascade;
drop table prestec cascade;
drop table quantitzacio cascade;
drop table concurs_socis cascade;
drop table material cascade;
drop table llibre cascade;
drop table accesori cascade;
drop table concurs cascade;

"""
