declare @tabla_visualizationCategory table (categories VARCHAR(50));
declare @tabla_name_machine table (name_machine VARCHAR(50));

INSERT INTO @tabla_visualizationCategory(categories)
VALUES ('combine'),('forageHarvester'),('tractor');

INSERT INTO @tabla_name_machine(name_machine)
VALUES ('Ardissono'),('Agronova 8500'),('FLOGNA S680'),('FLOGNA S680'), ('hj5670'), ('SOGMA S456');

DECLARE @count INT = 100;

while @count > 0
BEGIN
DECLARE @visualizationCategory VARCHAR(50) = (SELECT TOP 1 categories FROM @tabla_visualizationCategory ORDER BY NEWID()),
		@productkey VARCHAR(50) = (select CAST(CONVERT(INT, FLOOR(((100000000-10000000)* rand()) + 100000000)) AS varchar(50))),
		@engineSerialNumber VARCHAR(50) = dbo.fnCustomPass(15,'CN'),
		@telematicsState VARCHAR (50) = 'active',
		@guid_machine VARCHAR(50) = dbo.fn_alphanumeric_guion(25,'CN'),
		@modelYear VARCHAR(10) = CAST(FLOOR((2021-2014)* rand() + 2014) AS VARCHAR(10)),
		@id_machine VARCHAR(50) = dbo.fnCustomPass(6,'N'),
		@vin VARCHAR(50) = dbo.fnCustomPass(17,'CN'),
		@name_machine VARCHAR(50) = (SELECT TOP 1 name_machine FROM @tabla_name_machine ORDER BY NEWID()),
		@id_org VARCHAR(50) =  (SELECT TOP 1 id_org FROM organizacion ORDER BY NEWID()),
		@flag BIT = 0


		INSERT INTO [dbo].[machines]
           ([visualizationCategory]
           ,[productKey]
           ,[engineSerialNumber]
           ,[telematicsState]
           ,[guid_machine]
           ,[modelYear]
           ,[id_machine]
           ,[vin]
           ,[name_machine]
           ,[id_org]
           ,[FLAG])
		VALUES
           (@visualizationCategory
           ,@productkey
		   ,@engineSerialNumber
		   ,@telematicsState
		   ,@guid_machine
		   ,@modelYear
		   ,@id_machine
		   ,@vin
		   ,@name_machine
		   ,@id_org
		   ,@flag);
			
			SET @count = @count-1
END;
