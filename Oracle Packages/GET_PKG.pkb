/* Formatted on 5/28/2017 8:42:00 PM (QP5 v5.300) */
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
             WHERE GRUPO.GROUP_ID = 2;
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

    PROCEDURE GET_CITA_NA_DOCTOR (CITAS OUT SYS_REFCURSOR, DOCTOR IN INTEGER)
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
    END GET_CITA_NA_DOCTOR;

    PROCEDURE GET_CITA_P (CITAS OUT SYS_REFCURSOR, PACIENTE IN INTEGER)
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
             WHERE     tablaCitas.ID_PACIENTE = PACIENTE
                   AND tablaCitas.ACTIVO = 1;
    END GET_CITA_P;

    PROCEDURE GET_CITA_WITH_ID (CITAS OUT SYS_REFCURSOR, CITA_ID IN INTEGER)
    AS
    BEGIN
        OPEN CITAS FOR
            SELECT tablaCitas.ID_DENTISTA,
                   tablaCitas.ID_PACIENTE,
                   TO_CHAR (tablaCitas.FECHA_HORA),
                   tablaCitas.DETALLE
              FROM DIENTES.CITA tablaCitas
             WHERE tablaCitas.ID_CITA = CITA_ID AND tablaCitas.ACTIVO = 1;
    END GET_CITA_WITH_ID;

    PROCEDURE GET_CITA_NA_P (CITAS OUT SYS_REFCURSOR, PACIENTE IN INTEGER)
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
             WHERE     tablaCitas.ID_PACIENTE = PACIENTE
                   AND tablaCitas.ACEPTADA = 0
                   AND tablaCitas.ACTIVO = 1;
    END GET_CITA_NA_P;

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
            SELECT DISTINCT
                   AUTH.ID                                  AS PACIENTE_ID,
                   AUTH.FIRST_NAME || ' ' || AUTH.LAST_NAME AS PACIENTE
              FROM DIENTES.CITA  CITAS
                   INNER JOIN DIENTES.AUTH_USER AUTH
                       ON CITAS.ID_PACIENTE = AUTH.ID
             WHERE CITAS.ID_DENTISTA = DOCTOR;
    END GET_PACIENTES_DOCTOR;

    PROCEDURE GET_COUNTRY (PAIS OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN pais FOR
              SELECT paises.id_pais, paises.nombre
                FROM DIENTES.PAISES paises
            ORDER BY paises.id_pais ASC;
    END GET_COUNTRY;

    PROCEDURE GET_ESTADOS (pais IN INTEGER, estados OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN estados FOR
              SELECT estados.id_estado, estados.NOMBRE
                FROM DIENTES.ESTADO estados
               WHERE estados.ID_PAIS = pais
            ORDER BY estados.NOMBRE ASC;
    END GET_ESTADOS;

    PROCEDURE GET_CIUDADES (states IN INTEGER, ciudad OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN ciudad FOR
              SELECT city.ID_CIUDAD, city.NOMBRE
                FROM DIENTES.CIUDADES city
               WHERE city.ID_ESTADO = states
            ORDER BY city.nombre ASC;
    END GET_CIUDADES;

    PROCEDURE get_blood (blood OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN blood FOR
            SELECT bloodtype.ID_TIPO_SANGRE, bloodtype.NOMBRE
              FROM DIENTES.TIPO_SANGRE bloodtype;
    END;

    PROCEDURE get_user_info (usuario       IN     INTEGER,
                             informacion      OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN informacion FOR
            SELECT mainusuario.FIRST_NAME,
                   mainusuario.LAST_NAME,
                   mainusuario.EMAIL,
                   direccion.CALLE,
                   direccion.NUMERO,
                   direccion.ID_CIUDAD,
                   ciudad.ID_ESTADO,
                   estados.ID_PAIS,
                   secondusuario.CELULAR,
                   secondusuario.SEXO,
                   secondusuario.TIPO_SANGRE
              FROM dientes.auth_user  mainusuario
                   FULL OUTER JOIN DIENTES.USUARIOS secondusuario
                       ON mainusuario.ID = secondusuario.ID_USUARIO
                   FULL OUTER JOIN DIENTES.DIRECCIONES direccion
                       ON secondusuario.ID_DIRECCION = direccion.ID_DIRECCION
                   FULL OUTER JOIN DIENTES.CIUDADES ciudad
                       ON direccion.ID_CIUDAD = ciudad.ID_CIUDAD
                   FULL OUTER JOIN DIENTES.ESTADO estados
                       ON ciudad.ID_ESTADO = estados.ID_ESTADO
             WHERE mainusuario.ID = usuario;
    END get_user_info;

    PROCEDURE get_usernames (usernames OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN usernames FOR
            SELECT djangousers.ID, djangousers.USERNAME
              FROM DIENTES.AUTH_USER djangousers;
    END get_usernames;

    PROCEDURE get_groups (gruposdjango OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN gruposdjango FOR
            SELECT grupitos.ID, grupitos.NAME
              FROM DIENTES.AUTH_GROUP grupitos;
    END get_groups;

    PROCEDURE get_users (usernames OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN usernames FOR
            SELECT djangousers.ID, djangousers.USERNAME
              FROM DIENTES.AUTH_USER djangousers;
    END;

    PROCEDURE GET_USER (USUARIOID IN NUMBER, USERNAMES OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN USERNAMES FOR
            SELECT TABLAUSER.USERNAME,
                   TABLAUSER.FIRST_NAME,
                   TABLAUSER.LAST_NAME
              FROM DIENTES.AUTH_USER TABLAUSER
             WHERE TABLAUSER.ID = USUARIOID;
    END GET_USER;

    PROCEDURE GET_TRATAMIENTOS (OUT_TRATAMIENTOS OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN OUT_TRATAMIENTOS FOR
              SELECT TRATAMIENTOS.ID_TRATAMIENTO,
                     TRATAMIENTOS.NOMBRE,
                     ESPECIALIDAD.NOMBRE AS ESPECIALIDAD,
                     TRATAMIENTOS.COSTO
                FROM DIENTES.TRATAMIENTO TRATAMIENTOS
                     INNER JOIN DIENTES.ESPECIALIDADES ESPECIALIDAD
                         ON TRATAMIENTOS.ID_ESPECIALIDAD =
                                ESPECIALIDAD.ID_ESPECIALIDAD
            ORDER BY TRATAMIENTOS.NOMBRE ASC;
    END GET_TRATAMIENTOS;

    PROCEDURE GET_MATERIAL (OUT_MATERIAL OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN OUT_MATERIAL FOR
            SELECT MATERIALES.ID_MATERIAL, MATERIALES.NOMBRE
              FROM DIENTES.MATERIAL MATERIALES;
    END GET_MATERIAL;

    PROCEDURE GET_MATERIAL_TRATAMIENTO (
        ID_TRATAMIENTO_V   IN     NUMBER,
        OUT_MATERIAL          OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN OUT_MATERIAL FOR
            SELECT MATERIALES.ID_MATERIAL, MATERIALES.NOMBRE
              FROM DIENTES.TRATAMIENTO  TRATAMIENTOS
                   INNER JOIN DIENTES.TRATAMIENTO_MATERIAL TRAT_MAT
                       ON TRATAMIENTOS.ID_TRATAMIENTO =
                              TRAT_MAT.ID_TRATAMIENTO
                   INNER JOIN DIENTES.MATERIAL MATERIALES
                       ON TRAT_MAT.ID_MATERIAL = MATERIALES.ID_MATERIAL;
    END GET_MATERIAL_TRATAMIENTO;

    PROCEDURE GET_ESPECIALIDADES (ESPECIALIDAD OUT SYS_REFCURSOR)
    AS
    BEGIN
        OPEN ESPECIALIDAD FOR
            SELECT ESPEC.ID_ESPECIALIDAD, ESPEC.NOMBRE
              FROM DIENTES.ESPECIALIDADES ESPEC;
    END GET_ESPECIALIDADES;

    FUNCTION GET_GRUPO (USER_ID IN NUMBER)
        RETURN NUMBER
    IS
        ID_GRUPO   NUMBER;
    BEGIN
        SELECT grupos.GROUP_ID
          INTO ID_GRUPO
          FROM DIENTES.AUTH_USER  usuario
               INNER JOIN DIENTES.AUTH_USER_GROUPS grupos
                   ON usuario.ID = grupos.USER_ID
         WHERE usuario.ID = USER_ID AND ROWNUM = 1;
    EXCEPTION
        WHEN NO_DATA_FOUND
        THEN
            ID_GRUPO := 0;
            RETURN ID_GRUPO;
    END GET_GRUPO;

    PROCEDURE GET_ABONO (USER_ID     IN     NUMBER,
                         GRUPO              VARCHAR2,
                         OUT_ABONO      OUT SYS_REFCURSOR)
    IS
    BEGIN
        IF GRUPO = 'Doctores'
        THEN
            OPEN OUT_ABONO FOR
                SELECT *
                  FROM DIENTES.ABONOS  abono
                       INNER JOIN DIENTES.PAGOS PAGO
                           ON abono.ID_PAGO = PAGO.ID_PAGO
                 WHERE PAGO.ID_DENTISTA = USER_ID AND abono.ACTIVO = 1;
        ELSIF GRUPO = 'Administrador'
        THEN
            OPEN OUT_ABONO FOR
                SELECT abono.ID_ABONOS,
                       TRATA.NOMBRE,
                       abono.FECHA,
                       TRUNC (abono.COSTO, 2) AS COSTO,
                       abono.PAGADO
                  FROM DIENTES.ABONOS  abono
                       INNER JOIN DIENTES.TRATAMIENTO_PACIENTE TRAT
                           ON abono.ID_TRATAMIENTO_PACIENTE =
                                  TRAT.ID_TRATAMIENTOPACIENTE
                       INNER JOIN DIENTES.TRATAMIENTO TRATA
                           ON TRAT.ID_TRATAMIENTO = TRATA.ID_TRATAMIENTO
                 WHERE abono.ACTIVO = 1;
        ELSE
            OPEN OUT_ABONO FOR
                SELECT abono.ID_ABONOS,
                       TRATA.NOMBRE,
                       abono.FECHA,
                       TRUNC(abono.COSTO, 2) AS COSTO,
                       abono.PAGADO
                  FROM DIENTES.ABONOS  abono
                       INNER JOIN DIENTES.TRATAMIENTO_PACIENTE TRAT
                           ON abono.ID_TRATAMIENTO_PACIENTE =
                                  TRAT.ID_TRATAMIENTOPACIENTE
                       INNER JOIN DIENTES.TRATAMIENTO TRATA
                           ON TRAT.ID_TRATAMIENTO = TRATA.ID_TRATAMIENTO
                 WHERE TRAT.ID_PACIENTE = USER_ID AND abono.ACTIVO = 1;
        END IF;
    END GET_ABONO;

    PROCEDURE GET_PAGO (USER_ID     IN     NUMBER,
                        GRUPO              VARCHAR2,
                        OUT_PAGO     OUT SYS_REFCURSOR)
    AS
    BEGIN
        IF GRUPO = 'Doctores'
        THEN
            OPEN OUT_PAGO FOR
                SELECT *
                  FROM DIENTES.PAGOS PAGO
                 WHERE PAGO.ID_DENTISTA = USER_ID AND PAGO.ACTIVO = 1;
        ELSIF GRUPO = 'Administrador'
        THEN
            OPEN OUT_PAGO FOR
                SELECT *
                  FROM DIENTES.PAGOS PAGO
                 WHERE PAGO.ACTIVO = 1;
        ELSE
            OPEN OUT_PAGO FOR
                SELECT *
                  FROM DIENTES.PAGOS PAGO
                 WHERE PAGO.ID_PACIENTE = USER_ID AND PAGO.ACTIVO = 1;
        END IF;
    END GET_PAGO;
END GET_PKG;
/