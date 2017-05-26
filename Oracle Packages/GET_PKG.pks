/* Formatted on 5/25/2017 7:39:47 PM (QP5 v5.300) */
CREATE OR REPLACE PACKAGE DIENTES.GET_PKG
AS
    PROCEDURE GET_PACIENTE_CITA (PACIENTE OUT SYS_REFCURSOR);

    PROCEDURE GET_DOCTOR (DOCTOR OUT SYS_REFCURSOR);

    PROCEDURE GET_CITA_DOCTOR (CITAS OUT SYS_REFCURSOR, DOCTOR IN INTEGER);

    PROCEDURE GET_CITA_NA (CITAS OUT SYS_REFCURSOR, DOCTOR IN INTEGER);

    PROCEDURE GET_CITA_A_NA (CITAS OUT SYS_REFCURSOR);

    PROCEDURE GET_CITA_A (CITAS OUT SYS_REFCURSOR);

    PROCEDURE GET_HORARIO_DOC (DOCTOR IN NUMBER, HORAS OUT SYS_REFCURSOR);

    PROCEDURE GET_HORARIO_DIA (DOCTOR    IN     NUMBER,
                               DIA       IN     VARCHAR2,
                               HORADIA      OUT SYS_REFCURSOR);

    PROCEDURE GET_ADDRESS_ID (USUARIO      IN     NUMBER,
                              ADDRESS_ID      OUT SYS_REFCURSOR);

    PROCEDURE GET_USER_GROUP (USUARIO IN NUMBER, GRUPOCUR OUT SYS_REFCURSOR);

    PROCEDURE GET_PACIENTES_DOCTOR (DOCTOR      IN     NUMBER,
                                    PACIENTES      OUT SYS_REFCURSOR);

    PROCEDURE GET_COUNTRY (PAIS OUT SYS_REFCURSOR);

    PROCEDURE GET_ESTADOS (pais IN INTEGER, estados OUT SYS_REFCURSOR);

    PROCEDURE GET_CIUDADES (states IN INTEGER, ciudad OUT SYS_REFCURSOR);

    PROCEDURE get_blood (blood OUT SYS_REFCURSOR);

    PROCEDURE get_user_info (usuario       IN     INTEGER,
                             informacion      OUT SYS_REFCURSOR);

    PROCEDURE get_usernames (usernames OUT SYS_REFCURSOR);

    PROCEDURE get_groups (gruposdjango OUT SYS_REFCURSOR);

    PROCEDURE GET_USER (USUARIOID IN NUMBER, USERNAMES OUT SYS_REFCURSOR);

    PROCEDURE GET_TRATAMIENTOS (OUT_TRATAMIENTOS OUT SYS_REFCURSOR);
    
    PROCEDURE GET_MATERIAL (OUT_MATERIAL OUT SYS_REFCURSOR);

    PROCEDURE GET_MATERIAL_TRATAMIENTO (
        ID_TRATAMIENTO_V   IN     NUMBER,
        OUT_MATERIAL          OUT SYS_REFCURSOR);
END GET_PKG;
/