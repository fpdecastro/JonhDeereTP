CREATE TABLE organizacion(
	id_org VARCHAR(50),
	name VARCHAR(50),
	type_org VARCHAR(50),
	member BIT,
	PRIMARY KEY (id_org)
);

CREATE TABLE clientes(
	id_client VARCHAR(50),
	name_client VARCHAR(50),
	id_org VARCHAR(50),
	PRIMARY KEY (id_client)
);

ALTER TABLE clientes
ADD FOREIGN KEY (id_org) REFERENCES organizacion(id_org);

CREATE TABLE farms(
	id_farm VARCHAR(50),
	name VARCHAR(50),
	id_client VARCHAR(50),
	PRIMARY KEY (id_farm)
);

ALTER TABLE farms
ADD FOREIGN KEY (id_client) REFERENCES clientes(id_client)

CREATE TABLE fields(
	id_field VARCHAR(50),
	name VARCHAR(50),
	id_farm VARCHAR(50),
	PRIMARY KEY (id_field)
);

ALTER TABLE fields
ADD FOREIGN KEY (id_farm) REFERENCES farms(id_farm)

CREATE TABLE BOUNDARIES(
    boundaries_name VARCHAR(50),
    sourceType VARCHAR(50),
    createdTime VARCHAR(50),
    modifiedTime VARCHAR(50),
    archived BIT,
    id_boundaries VARCHAR(50),
    active BIT,
    irrigated BIT,
    id_field VARCHAR(50),
    PRIMARY KEY (id_boundaries)
);

ALTER TABLE BOUNDARIES
ADD FOREIGN KEY (id_field) REFERENCES fields(id_field)

CREATE TABLE area(
	id_area INT IDENTITY(1,1),
	valueAsDouble FLOAT,
	unit VARCHAR(50),
	id_boundaries VARCHAR(50)	
);

ALTER TABLE area
ADD FOREIGN KEY (id_boundaries) REFERENCES boundaries(id_boundaries);

CREATE TABLE operaciones(
    fieldOperationType VARCHAR(50),
    cropSeason VARCHAR(50),
    modifiedTime VARCHAR(50),
    startDate VARCHAR(50),
    endDate VARCHAR(50),
    cropName VARCHAR(50),
    id_operation VARCHAR(50),
    id_field VARCHAR(50),
    PRIMARY KEY (id_operation)
);

ALTER TABLE operaciones
ADD FOREIGN KEY (id_field) REFERENCES fields(id_field);

CREATE TABLE med_seeding(
	measurementName VARCHAR(50),
	measumerentCategory VARCHAR(50),
	area_value FLOAT,
	area_unit VARCHAR(10),
	totalMaterial_value FLOAT,
	totalMaterial_unit VARCHAR(50),
	averageMaterial_value FLOAT,
	averageMaterial_unit VARCHAR(50),
	id_operation VARCHAR(50)
);

CREATE TABLE med_harvest(
	measurementName VARCHAR(50),
	area_value FLOAT,
	area_unit VARCHAR(50),
	yield_value FLOAT,
	yield_unit VARCHAR(50),
	averageYield_value FLOAT,
	averageYield_unit VARCHAR(50),
	averageMoisture_value FLOAT,
	averageMoisture_unit VARCHAR(50),
	wetMass_value FLOAT,
	wetMass_unit VARCHAR(50),
	averageWetMass_value FLOAT,
	averageWetMass_unit VARCHAR(50),
	averageSpeed_value FLOAT,
	averageSpeed_unit VARCHAR(50),
	id_operation VARCHAR(50)
);

CREATE TABLE machines(
    visualizationCategory VARCHAR(50),
    productKey VARCHAR(50),
    engineSerialNumber VARCHAR(50),
    telematicsState VARCHAR(50),
    guid_machine VARCHAR(50),
    modelYear VARCHAR(10),
    id_machine VARCHAR(50),
    vin VARCHAR(50),
    name_machine VARCHAR(50),
    id_org VARCHAR(50),
    PRIMARY KEY (id_machine)
);

ALTER TABLE machines
ADD FOREIGN KEY (id_org) REFERENCES organizacion(id_org);

CREATE TABLE alertas(
	type_alert VARCHAR(50),
	duration_value VARCHAR(50),
	duration_unit VARCHAR(50),
	occurrences VARCHAR(50),
	engineHours_value FLOAT,
	engineHours_unit VARCHAR(50),
	machineLinearTime INT,
	bus VARCHAR(10),
	id_alert VARCHAR(50),
	time_alert VARCHAR(50),
	color VARCHAR(50),
	severity VARCHAR(50),
	acknowledgementStatus VARCHAR(2),
	ignored BIT,
	invisible BIT,
	id_machine VARCHAR (50),
	PRIMARY KEY(id_alert)		
);

ALTER TABLE alertas
ADD FOREIGN KEY (id_machine) REFERENCES machines(id_machine);

CREATE TABLE hoursOfOperation(
	type_hours VARCHAR(50),
	startDate VARCHAR(50),
	endDate	VARCHAR(50),
	engine_state BIT,
	id_machine VARCHAR(50),
);

ALTER TABLE hoursOfOperation
ADD FOREIGN KEY (id_machine) REFERENCES machines(id_machine);

CREATE TABLE engineHours(
	engineHours_value FLOAT,
	engineHours_unit VARCHAR(20),
	reportTime VARCHAR(50),
	id_machine VARCHAR(50)
);

ALTER TABLE engineHours
ADD FOREIGN KEY (id_machine) REFERENCES machines(id_machine);

CREATE TABLE historialLocation(
	point_lat FLOAT,
	point_lon FLOAT,
	eventTimestamp VARCHAR(50),
	gpsFixTimestamp VARCHAR(50),
	id_machine VARCHAR(50)
);
ALTER TABLE historialLocation
ADD FOREIGN KEY (id_machine) REFERENCES machines(id_machine);


