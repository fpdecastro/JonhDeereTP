DECLARE @count INT = 100

WHILE @count > 0
BEGIN
DECLARE @average_modified FLOAT = round((SELECT AVG(engineHours_value) FROM engineHours) - 2000 * (RAND()-RAND()),2),
		@engineHours_unit VARCHAR(20) = 'Hours'

DECLARE @menos_dias INT = ROUND(365*RAND(),0),
		@menos_horas INT = ROUND(24*RAND(),0),
		@menos_minutos INT = ROUND(24*RAND(),0),
		@id_machine VARCHAR(50) = (SELECT TOP 1 id_machine FROM machines ORDER BY NEWID()),
		@FLAG BIT = 0

DECLARE @reportTime DATETIME = DATEADD(DAY, - @menos_dias, GETDATE())
SET @reportTime = DATEADD(HOUR, + @menos_horas, @reportTime)
SET @reportTime = DATEADD(MINUTE, + @menos_minutos, @reportTime)
declare @reportTime_varchar VARCHAR(50) = (SELECT convert(VARCHAR(50), @reportTime, 126))

INSERT INTO [dbo].[engineHours]
           ([engineHours_value]
           ,[engineHours_unit]
           ,[reportTime]
           ,[id_machine]
           ,[flag])
     VALUES
           (@average_modified
		   ,@engineHours_unit
		   ,@reportTime_varchar
		   ,@id_machine
		   ,@FLAG);
SET @count = @count - 1 

END
