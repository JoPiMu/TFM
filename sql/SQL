CREATE EXTENSION IF NOT EXISTS postgis;

DROP VIEW IF EXISTS comercios_poblacion_view;
DROP TABLE IF EXISTS secciones_indicadores;
DROP TABLE IF EXISTS indicadores;
DROP TABLE IF EXISTS comercios;

CREATE TABLE comercios (
    id SERIAL PRIMARY KEY,
    key VARCHAR(60),
    type VARCHAR(60),
    name VARCHAR(60),
    lon DECIMAL(8, 6) NOT NULL,
    lat DECIMAL(9, 6) NOT NULL,
    geom geometry (Point, 4326)
);

CREATE TABLE indicadores (
    ccaa VARCHAR(2),
    cpro VARCHAR(2),
    cmun VARCHAR(3),
    dist VARCHAR(2),
    secc VARCHAR(3),
    t1_1 INTEGER
);

CREATE TABLE secciones_indicadores (
    id SERIAL PRIMARY KEY,
    Codigo_Seccion_Censal VARCHAR(3),
    Codigo_Distrito VARCHAR(2),
    Codigo_Municipio VARCHAR(3),
    Codigo_Provincia VARCHAR(2),
    Codigo_Comunidad_Autonoma VARCHAR(2),
    Provincia VARCHAR(50),
    Comunidad_Autonoma VARCHAR(50),
    Municipio VARCHAR(50),
    Poblacion INTEGER,
    geom GEOMETRY
);

UPDATE comercios
SET geom=ST_SetSRID (ST_MakePoint (lon, lat), 4326);

COPY indicadores (ccaa, cpro, cmun, dist, secc, t1_1)
FROM 'path/to/your/csv/file.csv' DELIMITER ',' CSV HEADER;

INSERT INTO secciones_indicadores (
    Codigo_Seccion_Censal,
    Codigo_Distrito,
    Codigo_Municipio,
    Codigo_Provincia,
    Codigo_Comunidad_Autonoma,
    Provincia,
    Comunidad_Autonoma,
    Municipio,
    Poblacion,
    geom
)
SELECT
    s.CSEC,
    s.CDIS,
    s.CMUN,
    s.CPRO,
    s.CCA,
    s.NPRO,
    s.NCA,
    s.NMUN,
    i.t1_1,
    s.geom
FROM
    "secciones" s
JOIN
    "indicadores" i 
ON
    s.CPRO=i.cpro
    AND s.CMUN=i.cmun
    AND s.CSEC=i.secc
    AND s.cdis=i.dist
WHERE
    s.CCA=i.ccaa
    AND s.CPRO=i.cpro
    AND s.CMUN=i.cmun;

UPDATE secciones_indicadores
SET geom=ST_SetSRID (geom, 25830);

UPDATE secciones_indicadores
SET geom=St_Transform (geom, 4326);

CREATE VIEW comercios_poblacion_view AS
SELECT 
    row_number() OVER () AS id,
    si.Comunidad_Autonoma,
    si.Provincia,
    si.Municipio,
    si.Codigo_Distrito,
    si.Codigo_Seccion_Censal,
    si.Poblacion,
    COUNT(c.id) AS Num_Locales,
    ROUND(((COUNT(c.id) * 100.0) / si.Poblacion)::NUMERIC, 2) AS Locales_100hab,
    si.geom
FROM 
    secciones_indicadores si
LEFT JOIN 
    comercios c
ON 
    ST_Intersects(si.geom, c.geom)
GROUP BY 
    si.Comunidad_Autonoma,
    si.Provincia,
    si.Municipio,
    si.Codigo_Distrito,
    si.Codigo_Seccion_Censal,
    si.Poblacion,
    si.geom;

------ COMPROBACIONES -------
SELECT * FROM secciones_indicadores;
SELECT * FROM secciones;
	
SELECT * FROM comercios;

SELECT * FROM comercios_poblacion_view;

SELECT ST_SRID(geom) FROM secciones_indicadores
GROUP BY ST_SRID;

SELECT St_Astext(geom) FROM secciones_indicadores;
-----------------------------
