--Me devuelve una cadena alphanumerica, de números o letras

CREATE FUNCTION fn_alphanumeric_guion 
(    
    @size AS INT, 
    @op AS VARCHAR(2) 
)
RETURNS VARCHAR(62)
AS
BEGIN    

    DECLARE @chars AS VARCHAR(52),
            @numbers AS VARCHAR(10),
            @strChars AS VARCHAR(62),        
            @strPass AS VARCHAR(62),
            @index AS INT,
            @cont AS INT

    SET @strPass = ''
    SET @strChars = ''    
    SET @chars = 'ABCDEF-GHIJKLM-NOPQRSTUVWXYZ'
    SET @numbers = '01234-56789-'

    SET @strChars = CASE @op WHEN 'C' THEN @chars --Letras
                        WHEN 'N' THEN @numbers --Números
                        WHEN 'CN' THEN @chars + @numbers --Ambos (Letras y Números)
                        ELSE '------'
                    END

    SET @cont = 0
    WHILE @cont < @size
    BEGIN
        SET @index = ceiling( ( SELECT rnd1 FROM vwRandom1 ) * (len(@strChars)))--Uso de la vista para el Rand() y no generar error.
        SET @strPass = @strPass + substring(@strChars, @index, 1)
        SET @cont = @cont + 1
    END    
        
    RETURN @strPass

END
GO

CREATE VIEW vwRandom1
AS
SELECT RAND() as Rnd1
GO 

SELECT dbo.fn_alphanumeric_guion(25,'CN');