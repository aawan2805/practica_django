from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Poner checks
# Poner null/not null
# Poner primary key
# Poner FK si son mas de una
# Poner ON DELTE, ON UPDATE

class Biblioteca(models.Model):
	codi = models.CharField(unique=True,
							max_length=10,
							null=False,
							blank=False)
	nom = models.CharField(max_length=50,
						   null=False,
						   blank=False)

	def __str__(self):
		print("Biblioteca({}, {})".format(self.codi, self.name))

	class Meta:
		db_table = "biblioteca"


class CodiPostal(models.Model):
	codi = models.CharField(unique=True,
							max_length=5,
							null=False,
							blank=False)
	biblioteca = models.OneToOneField(Biblioteca,
									  null=False,
									  blank=False,
									  on_delete=models.RESTRICT,
									  db_column="biblioteca",
									  related_name="codi_postal")
	def __str__(self):
		print("CodiPostal({})".format(self.codi))

	class Meta:
		db_table = "codipostal"


class Horari(models.Model):
	dia = models.CharField(max_length=10,
						   null=False,
						   blank=False) # Y si yo le doy los choices?
	hora_obertura = models.CharField(max_length=2,
									 null=False,
									 blank=False) # Char of 2 or integer?
	hora_tancament = models.CharField(max_length=2,
									  null=False,
									  blank=False) # Char of 2 or integer?
	biblioteca = models.ForeignKey(Biblioteca,
								   null=False,
								   blank=False,
								   on_delete=models.CASCADE,
								   db_column="biblioteca",
								   related_name="horaris")
	def __str__(self):
		print("Horari({} desde {} fins a {})".format(self.dia, self.hora_obertura, self.hora_tancament))

	class Meta:
		db_table = "horari"


class Soci(models.Model):
	dni = models.CharField(unique=True,
						   max_length=9,
						   null=False,
						   blank=False)
	nom = models.CharField(max_length=50,
						   null=False,
						   blank=False) # Null true sta be? o ha de estar en RS?
	cognom = models.CharField(max_length=50,
							  null=False,
							  blank=False) # Null true sta be? o ha de estar en RS?
	data_naixement = models.DateField(null=False,
									  blank=False)
	biblioteca = models.ForeignKey(Biblioteca,
								   null=False,
								   blank=False,
								   on_delete=models.RESTRICT,
								   db_column="biblioteca",
								   related_name="socis")
	def __str__(self):
		print("Soci({}, {}, {}, {})".format(self.dni, self.nom, self.cognom, self.data_naixement))

	class Meta:
		db_table = "soci"


class Concurs(models.Model):
	data = models.DateField(unique=True,
							null=False,
							blank=False)
	edat_minima = models.IntegerField(null=False,
									  blank=False,
									  validators=[MinValueValidator(1), MaxValueValidator(120)]) # max_value hace falta? no esta en las RSs
	biblioteca1 = models.ForeignKey(Biblioteca,
									null=False,
									blank=False,
									on_delete=models.RESTRICT,
									db_column="biblioteca1",
									related_name='concursos_bib_1')
	biblioteca2 = models.ForeignKey(Biblioteca,
									null=False,
									blank=False,
									on_delete=models.RESTRICT,
									db_column="biblioteca2",
									related_name='concursos_bib_2')
	socis = models.ManyToManyField(Soci, related_name="concursos") # La interrelació 1..* - 1..* entre Soci i Concurs

	def __str__(self):
		print("Concurs({})".format(self.data))

	class Meta:
		db_table = "concurs"


class Material(models.Model):
	codi_barres = models.CharField(unique=True,
								  max_length=13,
								  null=False,
								  blank=False)
	nom = models.CharField(max_length=50,
						   null=False,
						   blank=False)
	quantitats = models.ManyToManyField(Biblioteca, through='Quantitzacio')

	def __str__(self):
		print("Material({}, {})".format(self.codi_barres, self.nom))

	class Meta:
		db_table = "material"


class Llibre(models.Model): # Cómo hago que sea una CP??? y tengo que hacer que apunte al ID?????
	codi_barres = models.ForeignKey(Material,
								   unique=True,
								   null=False,
								   blank=False,
								   on_delete=models.CASCADE,
								   db_column="codi_barres",
								   related_name="llibre") # Puedo usar 1to1?
	autor = models.CharField(max_length=50,
							 null=True,
							 blank=True) # null true? o tiene que estar en RS?

	def __str__(self):
		print("Llibre({}, {})".format(self.codi_barres, self.autor))

	class Meta:
		db_table = "llibre"


class Accesori(models.Model):
	codi_barres = models.ForeignKey(Material,
								   unique=True,
								   null=False,
								   blank=False,
								   on_delete=models.CASCADE,
								   db_column="codi_barra",
								   related_name="accesori")
	tipus = models.CharField(max_length=50,
							 null=True,
							 blank=True) # null true? o tiene que estar en RS?

	def __str__(self):
		print("Accesori({}, {})".format(self.codi_barres, self.tipus))

	class Meta:
		db_table = "accesori"


class Prestec(models.Model):
	data_retorn = models.DateField(null=True,
								   blank=True)
	data_limit = models.DateField(null=False,
								  blank=False)
	material = models.ForeignKey(Material,
								 null=False,
								 blank=False,
								 on_delete=models.RESTRICT,
								 db_column="material",
								 related_name="prestecs")
	soci = models.ForeignKey(Soci,
							 null=False,
							 blank=False,
							 on_delete=models.CASCADE,
							 db_column="soci",
							 related_name="prestecs") # SI borro los socios borro tambien el prestamo. No me interesa mantener historial.??
	prestec_demanat = models.ForeignKey(Biblioteca,
										null=True,
										blank=True,
										on_delete=models.RESTRICT,
										db_column="prestec_demanat",
										related_name="prestec_prestat")
	data_estimacio = models.DateField(null=True,
									  blank=True)

	class Meta:
		db_table = "prestec"


class Quantitzacio(models.Model):
	material = models.ForeignKey(Material,
								 db_column="material",
								 on_delete=models.CASCADE)
	biblioteca = models.ForeignKey(Biblioteca,
								   db_column="biblioteca",
								   on_delete=models.CASCADE)
	quantitat = models.IntegerField(null=False,
									blank=False,
									validators=[MinValueValidator(0)])

	class Meta:
		db_table = "quantitzacio"
		unique_together = ('material', 'biblioteca')
