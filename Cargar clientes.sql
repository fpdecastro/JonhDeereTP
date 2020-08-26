DECLARE @data VARCHAR(MAX);

SELECT @data = BulkColumn FROM OPENROWSET(BULK 'C:\CarpetaBaseDelosJSON\478064.json', SINGLE_CLOB) JSON

--SELECT BulkColumn,
--	charindex('organizations',BulkColumn),
--	substring(BulkColumn,charindex('organizations',BulkColumn)+14,6 ) FROM OPENROWSET(BULK 'C:\Users\MbelenC\Documents\JohnDeereClientes\419718.json', SINGLE_CLOB) JSON

DECLARE @inicioTotal INT = charindex('total',@data) + 8;
DECLARE @finalTotal INT = charindex(',',@data,charindex('total',@data)+8)


--La cantidad se supone que deberia servir para cualquier entidad
DECLARE @cantidad INT= ( CASE
						WHEN @inicioTotal = @finalTotal THEN 1
						ELSE CAST(SUBSTRING(@data,@inicioTotal, @finalTotal-@inicioTotal) AS INT)
						END);
DECLARE @actual INT = 0;

DECLARE @id varchar(100),
		@colum_id VARCHAR(100);
DECLARE @name NVARCHAR(100),
		@colum_name VARCHAR(100);
		
--En este caso se busca clientes POR ORGANIZACION, en cada archivo los clientes perteneces a una misma org y se puede buscar en la linea del link que sale en el archivo json
--Si se entra por maquina habria que buscar la palabra machines y analizar en donde empezaria el id a partir de esa palabra
DECLARE @organizacion INT = substring(@data,charindex('organizations',@data)+14,6 )

WHILE @actual<@cantidad
BEGIN

SET @colum_id = (SELECT JSON_VALUE (@data, CONCAT('$.values[',@actual,'].id')))
SET @id = (SELECT CASE 
				WHEN @colum_id LIKE '' THEN NULL
				ELSE @colum_id
				END)

SET @colum_name = (SELECT JSON_VALUE (@data, CONCAT('$.values[',@actual,'].name')))
SET @name = (SELECT CASE 
				WHEN @colum_name LIKE '' THEN NULL
				ELSE @colum_name
				END)

INSERT INTO JD_CLIENTES(id, name, id_organizacion) VALUES (@id, @name, @organizacion)

SET @actual = @actual + 1
END