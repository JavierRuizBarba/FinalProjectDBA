CREATE OR REPLACE PACKAGE DIENTES.GET_PKG
AS
PROCEDURE GET_PACIENTE_CITA(PACIENTE OUT SYS_REFCURSOR);
END GET_PKG;
/