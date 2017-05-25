/* Formatted on 5/23/2017 2:31:05 PM (QP5 v5.300) */
CREATE OR REPLACE PACKAGE BODY DIENTES.GET_PKG
AS
    PROCEDURE GET_PACIENTE_CITA (PACIENTE OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN PACIENTE FOR
            SELECT paciente.ID, FIRST_NAME, LAST_NAME
              FROM DIENTES.AUTH_USER  paciente
                   LEFT JOIN DIENTES.AUTH_USER_GROUPS grupo
                       ON paciente.ID = grupo.USER_ID
             WHERE grupo.USER_ID IS NULL;
    END GET_PACIENTE_CITA;

    PROCEDURE GET_DOCTOR (DOCTOR OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN DOCTOR FOR
            SELECT DOCTORES.ID, DOCTORES.FIRST_NAME, DOCTORES.LAST_NAME
              FROM DIENTES.AUTH_USER  DOCTORES
                   INNER JOIN DIENTES.AUTH_USER_GROUPS GRUPO
                       ON DOCTORES.ID = GRUPO.USER_ID
             WHERE GRUPO.GROUP_ID = 1;
    END GET_DOCTOR;

    PROCEDURE GET_CITA_DOCTOR (CITAS OUT SYS_REFCURSOR, DOCTOR IN INTEGER)
    AS
    BEGIN
        OPEN CITAS FOR
            SELECT tablaCitas.ID_CITA,
                   pacientes.FIRST_NAME || ' ' || pacientes.LAST_NAME AS PACIENTE,
                   dentistas.FIRST_NAME || ' ' || dentistas.LAST_NAME AS DENTISTA,
                   tablaCitas.FECHA_HORA,
                   tablaCitas.ACEPTADA,
                   tablaCitas.DETALLE,
                   tablaCitas.ASISTIO
              FROM DIENTES.CITA  tablaCitas
                   INNER JOIN DIENTES.AUTH_USER pacientes
                       ON tablaCitas.ID_PACIENTE = pacientes.ID
                   INNER JOIN DIENTES.AUTH_USER dentistas
                       ON tablaCitas.ID_DENTISTA = dentistas.ID
             WHERE tablaCitas.ID_DENTISTA = DOCTOR AND tablaCitas.ACTIVO = 1;
    END GET_CITA_DOCTOR;

    PROCEDURE GET_CITA_NA (CITAS OUT SYS_REFCURSOR, DOCTOR IN INTEGER)
    AS
    BEGIN
        OPEN CITAS FOR
            SELECT tablaCitas.ID_CITA,
                   pacientes.FIRST_NAME || ' ' || pacientes.LAST_NAME AS PACIENTE,
                   dentistas.FIRST_NAME || ' ' || dentistas.LAST_NAME AS DENTISTA,
                   tablaCitas.FECHA_HORA,
                   tablaCitas.DETALLE,
                   tablaCitas.ASISTIO
              FROM DIENTES.CITA tablaCitas
              INNER JOIN DIENTES.AUTH_USER pacientes
                       ON tablaCitas.ID_PACIENTE = pacientes.ID
                   INNER JOIN DIENTES.AUTH_USER dentistas
                       ON tablaCitas.ID_DENTISTA = dentistas.ID
             WHERE     tablaCitas.ID_DENTISTA = DOCTOR
                   AND tablaCitas.ACEPTADA = 0 AND tablaCitas.ACTIVO = 1;
    END GET_CITA_NA;

    PROCEDURE GET_CITA_A_NA (CITAS OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN CITAS FOR
            SELECT *
              FROM DIENTES.CITA tablaCitas
             WHERE tablaCitas.ACEPTADA = 0;
    END GET_CITA_A_NA;

    PROCEDURE GET_CITA_A (CITAS OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN CITAS FOR
            SELECT *
              FROM DIENTES.CITA tablaCitas;
    END GET_CITA_A;
    
    Procedure GET_HORARIO_DOC(DOCTOR IN NUMBER, HORAS OUT SYS_REFCURSOR)
    IS
    HORARIO_ID NUMBER;
    BEGIN
        SELECT USUARIO.HORARIO INTO HORARIO_ID FROM DIENTES.USUARIOS USUARIO WHERE USUARIO.ID_USUARIO = DOCTOR;
        OPEN HORAS FOR
            SELECT HORARIO.LUNES, HORARIO.MARTES, HORARIO.MIERCOLES, HORARIO.JUEVES, HORARIO.VIERNES,
            HORARIO.SABADO, HORARIO.DOMINGO FROM DIENTES.HORARIOS HORARIO WHERE HORARIO.ID_HORARIO = HORARIO_ID;
    END GET_HORARIO_DOC;
    
    PROCEDURE GET_HORARIO_DIA(DOCTOR IN NUMBER, DIA IN VARCHAR2, HORADIA OUT sys_refcursor)
    IS
    HORARIO_ID NUMBER;
    BEGIN
        SELECT TABLAUSER.HORARIO INTO HORARIO_ID FROM DIENTES.USUARIOS TABLAUSER WHERE TABLAUSER.ID_USUARIO = DOCTOR;
        open horadia for
            SELECT * FROM DIENTES.HORARIOS HORA WHERE HORA.ID_HORARIO = HORARIO_ID;
    END GET_HORARIO_DIA;
    
    Procedure GET_ADDRESS_ID(USUARIO IN NUMBER, ADDRESS_ID OUT sys_refcursor)
    AS
    BEGIN
    open address_id for
        Select secondusers.ID_DIRECCION from dientes.usuarios secondusers where secondusers.ID_USUARIO = USUARIO;
    END GET_ADDRESS_ID;
    
    PROCEDURE GET_USER_GROUP(USUARIO IN NUMBER, GRUPOCUR OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN GRUPOCUR FOR
            SELECT GRUPOUSUARIO.ID FROM DIENTES.AUTH_USER_GROUPS GRUPOUSUARIO WHERE GRUPOUSUARIO.USER_ID = USUARIO;
    END GET_USER_GROUP;
END GET_PKG;
/
variable rc refcursor;
exec dientes.get_pkg.get_USER_GROUP(8, :rc);
print rc;
















