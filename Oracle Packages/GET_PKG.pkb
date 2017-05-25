/* Formatted on 5/25/2017 11:23:47 AM (QP5 v5.300) */
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
                   pacientes.FIRST_NAME || ' ' || pacientes.LAST_NAME
                       AS PACIENTE,
                   dentistas.FIRST_NAME || ' ' || dentistas.LAST_NAME
                       AS DENTISTA,
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
                   pacientes.FIRST_NAME || ' ' || pacientes.LAST_NAME
                       AS PACIENTE,
                   dentistas.FIRST_NAME || ' ' || dentistas.LAST_NAME
                       AS DENTISTA,
                   tablaCitas.FECHA_HORA,
                   tablaCitas.DETALLE,
                   tablaCitas.ASISTIO
              FROM DIENTES.CITA  tablaCitas
                   INNER JOIN DIENTES.AUTH_USER pacientes
                       ON tablaCitas.ID_PACIENTE = pacientes.ID
                   INNER JOIN DIENTES.AUTH_USER dentistas
                       ON tablaCitas.ID_DENTISTA = dentistas.ID
             WHERE     tablaCitas.ID_DENTISTA = DOCTOR
                   AND tablaCitas.ACEPTADA = 0
                   AND tablaCitas.ACTIVO = 1;
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

    PROCEDURE GET_HORARIO_DOC (DOCTOR IN NUMBER, HORAS OUT SYS_REFCURSOR)
    IS
        HORARIO_ID   NUMBER;
    BEGIN
        SELECT USUARIO.HORARIO
          INTO HORARIO_ID
          FROM DIENTES.USUARIOS USUARIO
         WHERE USUARIO.ID_USUARIO = DOCTOR;

        OPEN HORAS FOR
            SELECT HORARIO.LUNES,
                   HORARIO.MARTES,
                   HORARIO.MIERCOLES,
                   HORARIO.JUEVES,
                   HORARIO.VIERNES,
                   HORARIO.SABADO,
                   HORARIO.DOMINGO
              FROM DIENTES.HORARIOS HORARIO
             WHERE HORARIO.ID_HORARIO = HORARIO_ID;
    END GET_HORARIO_DOC;

    PROCEDURE GET_HORARIO_DIA (DOCTOR    IN     NUMBER,
                               DIA       IN     VARCHAR2,
                               HORADIA      OUT SYS_REFCURSOR)
    IS
        HORARIO_ID   NUMBER;
    BEGIN
        SELECT TABLAUSER.HORARIO
          INTO HORARIO_ID
          FROM DIENTES.USUARIOS TABLAUSER
         WHERE TABLAUSER.ID_USUARIO = DOCTOR;

        OPEN horadia FOR
            SELECT *
              FROM DIENTES.HORARIOS HORA
             WHERE HORA.ID_HORARIO = HORARIO_ID;
    END GET_HORARIO_DIA;

    PROCEDURE GET_ADDRESS_ID (USUARIO      IN     NUMBER,
                              ADDRESS_ID      OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN address_id FOR
            SELECT secondusers.ID_DIRECCION
              FROM dientes.usuarios secondusers
             WHERE secondusers.ID_USUARIO = USUARIO;
    END GET_ADDRESS_ID;

    PROCEDURE GET_USER_GROUP (USUARIO IN NUMBER, GRUPOCUR OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN GRUPOCUR FOR
            SELECT GRUPOUSUARIO.ID
              FROM DIENTES.AUTH_USER_GROUPS GRUPOUSUARIO
             WHERE GRUPOUSUARIO.USER_ID = USUARIO;
    END GET_USER_GROUP;

    PROCEDURE GET_PACIENTES_DOCTOR (DOCTOR      IN     NUMBER,
                                    PACIENTES      OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN pacientes FOR
            SELECT Distinct AUTH.FIRST_NAME, AUTH.LAST_NAME
              FROM DIENTES.CITA  CITAS
                   INNER JOIN DIENTES.AUTH_USER AUTH
                       ON CITAS.ID_PACIENTE = AUTH.ID
             WHERE CITAS.ID_DENTISTA = DOCTOR;
    END GET_PACIENTES_DOCTOR;
PROCEDURE GET_COUNTRY(PAIS OUT SYS_REFCURSOR)
as
begin
    open pais for
        Select paises.id_pais, paises.nombre from DIENTES.PAISES paises order by paises.id_pais asc;
end GET_COUNTRY;
PROCEDURE GET_ESTADOS(pais in integer, estados out sys_refcursor)
as
begin
    open estados for
        Select estados.id_estado, estados.NOMBRE from DIENTES.ESTADO estados where estados.ID_PAIS = pais order by estados.NOMBRE asc;
end GET_ESTADOS;
PROCEDURE GET_CIUDADES(states in integer, ciudad out sys_refcursor)
as
begin
    open ciudad for
        Select city.ID_CIUDAD, city.NOMBRE from DIENTES.CIUDADES city where city.ID_ESTADO = states order by city.nombre asc;
end GET_CIUDADES;

procedure get_blood(blood out sys_refcursor)
as
begin

    open blood for
        select bloodtype.ID_TIPO_SANGRE, bloodtype.NOMBRE from DIENTES.TIPO_SANGRE bloodtype;
end;
procedure get_user_info(usuario in integer, informacion out sys_refcursor)
as
begin
    open informacion for
        select mainusuario.FIRST_NAME, mainusuario.LAST_NAME, mainusuario.EMAIL, direccion.CALLE, direccion.NUMERO, direccion.ID_CIUDAD, ciudad.ID_ESTADO,
        estados.ID_PAIS, secondusuario.CELULAR, secondusuario.SEXO, secondusuario.TIPO_SANGRE
        from dientes.auth_user mainusuario full outer join DIENTES.USUARIOS secondusuario on mainusuario.ID=secondusuario.ID_USUARIO 
        full outer join DIENTES.DIRECCIONES direccion on secondusuario.ID_DIRECCION = direccion.ID_DIRECCION full outer join DIENTES.CIUDADES ciudad
        on direccion.ID_CIUDAD = ciudad.ID_CIUDAD full outer join DIENTES.ESTADO estados on ciudad.ID_ESTADO = estados.ID_ESTADO
        where mainusuario.ID = usuario;
end get_user_info;
procedure get_usernames (usernames out sys_refcursor)
as
begin
    open usernames for
        select djangousers.ID, djangousers.USERNAME from DIENTES.AUTH_USER djangousers;
end get_usernames;

procedure get_groups (gruposdjango out sys_refcursor)
as
begin
    open gruposdjango for
        select grupitos.ID, grupitos.NAME from DIENTES.AUTH_GROUP grupitos;
end get_groups;
END GET_PKG;
/

