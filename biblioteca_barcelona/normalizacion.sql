BEGIN;
--
-- Create model Biblioteca
--
CREATE TABLE "biblioteca" (
	"codi" varchar(20) NOT NULL PRIMARY KEY, 
	"nom" varchar(50) NOT NULL
);
--
-- Create model Concurs
--
CREATE TABLE "concurs" (
	"data" date NOT NULL PRIMARY KEY, 
	"edat_minima" integer NOT NULL, 
	"biblioteca1_id" varchar(20) NOT NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED, 
	"biblioteca2_id" varchar(20) NOT NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Material
--
CREATE TABLE "material" (
	"codi_barra" varchar(13) NOT NULL PRIMARY KEY, 
	"nom" varchar(50) NOT NULL
);
--
-- Create model Accesori
--
CREATE TABLE "accesori" (
	"codi_barra_id" varchar(13) NOT NULL PRIMARY KEY REFERENCES "material" ("codi_barra") DEFERRABLE INITIALLY DEFERRED, 
	"tipus" varchar(50) NULL
);
--
-- Create model Llibre
--
CREATE TABLE "llibre" (
	"codi_barra_id" varchar(13) NOT NULL PRIMARY KEY REFERENCES "material" ("codi_barra") DEFERRABLE INITIALLY DEFERRED, 
	"autor" varchar(50) NULL
);
--
-- Create model Soci
--
CREATE TABLE "soci" (
	"dni" varchar(9) NOT NULL PRIMARY KEY, 
	"nom" varchar(50) NULL, 
	"cognom" varchar(50) NULL, 
	"data_naixement" date NOT NULL, 
	"biblioteca_id" varchar(20) NOT NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Prestec
--
CREATE TABLE "prestec" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"data_retorn" date NOT NULL, 
	"data_limit" date NOT NULL, 
	"data_estimacio" date NULL, 
	"material_id" varchar(13) NULL REFERENCES "material" ("codi_barra") DEFERRABLE INITIALLY DEFERRED, 
	"prestec_demanat_id" varchar(20) NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED, 
	"soci_id" varchar(9) NULL REFERENCES "soci" ("dni") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Horari
--
CREATE TABLE "horari" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"dia" varchar(10) NOT NULL, 
	"hora_obertura" varchar(2) NOT NULL, 
	"hora_tancament" varchar(2) NOT NULL, 
	"biblioteca_id" varchar(20) NOT NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model CodiPostal
--
CREATE TABLE "codipostal" (
	"codi" varchar(5) NOT NULL PRIMARY KEY, 
	"biblioteca_id" varchar(20) NOT NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Quantitzacio
--
CREATE TABLE "quantitzacio" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"quantitat" integer NOT NULL, 
	"biblioteca_id" varchar(20) NOT NULL REFERENCES "biblioteca" ("codi") DEFERRABLE INITIALLY DEFERRED, 
	"material_id" varchar(13) NOT NULL REFERENCES "material" ("codi_barra") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model ConcursSoci
--
CREATE TABLE "concurssoci" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"concurs_id" date NOT NULL REFERENCES "concurs" ("data") DEFERRABLE INITIALLY DEFERRED, 
	"soci_id" varchar(9) NOT NULL REFERENCES "soci" ("dni") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "concurs_biblioteca1_id_cdf09a32" ON "concurs" ("biblioteca1_id");
CREATE INDEX "concurs_biblioteca2_id_77d226c2" ON "concurs" ("biblioteca2_id");
CREATE INDEX "soci_biblioteca_id_c1e3775c" ON "soci" ("biblioteca_id");
CREATE INDEX "prestec_material_id_429f34ef" ON "prestec" ("material_id");
CREATE INDEX "prestec_prestec_demanat_id_9f842f99" ON "prestec" ("prestec_demanat_id");
CREATE INDEX "prestec_soci_id_2c827e8e" ON "prestec" ("soci_id");
CREATE INDEX "horari_biblioteca_id_cd0315d6" ON "horari" ("biblioteca_id");
CREATE INDEX "codipostal_biblioteca_id_ea789946" ON "codipostal" ("biblioteca_id");
CREATE UNIQUE INDEX "quantitzacio_biblioteca_id_material_id_2e918437_uniq" ON "quantitzacio" ("biblioteca_id", "material_id");
CREATE INDEX "quantitzacio_biblioteca_id_12c36b0c" ON "quantitzacio" ("biblioteca_id");
CREATE INDEX "quantitzacio_material_id_e4a4287e" ON "quantitzacio" ("material_id");
CREATE UNIQUE INDEX "concurssoci_concurs_id_soci_id_a1b0ff4d_uniq" ON "concurssoci" ("concurs_id", "soci_id");
CREATE INDEX "concurssoci_concurs_id_5f3cb674" ON "concurssoci" ("concurs_id");
CREATE INDEX "concurssoci_soci_id_de21843f" ON "concurssoci" ("soci_id");
COMMIT;
