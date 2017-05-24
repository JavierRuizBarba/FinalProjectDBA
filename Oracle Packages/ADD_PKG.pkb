CREATE OR REPLACE PACKAGE BODY DIENTES.ADD_PKG
AS
    PROCEDURE ADD_ALERGIA (OUT_ALERGIA OUT NUMBER, ALERGIA VARCHAR2)
    IS
        ALERGIA_ID   NUMBER;
    BEGIN
        ALERGIA_ID := DIENTES.ALERGIAS_SQ.NEXTVAL;

        INSERT INTO DIENTES.ALERGIAS (ID_ALERGIA, NOMBRE)
             VALUES (ALERGIA_ID, ALERGIA);
    END ADD_ALERGIA;

    PROCEDURE ADD_ABONO (OUT_ABONO                 OUT NUMBER,
                         PAGADO                        NUMBER,
                         ID_TRATAMIENTO_PACIENTE       NUMBER,
                         COSTO                         NUMBER,
                         FECHA                         DATE,
                         ID_PAGO                       NUMBER)
    IS
        ABONO_ID   NUMBER;
    BEGIN
        ABONO_ID := DIENTES.ABONOS_SQ.NEXTVAL;

        INSERT INTO DIENTES.ABONOS (ID_ABONOS,
                                    PAGADO,
                                    ID_TRATAMIENTO_PACIENTE,
                                    COSTO,
                                    FECHA,
                                    ID_PAGO)
             VALUES (ABONO_ID,
                     PAGADO,
                     ID_TRATAMIENTO_PACIENTE,
                     COSTO,
                     FECHA,
                     ID_PAGO);
    END ADD_ABONO;

    PROCEDURE ADD_CAMBIO (OUT_CAMBIO         OUT NUMBER,
                          ID_MONEDA_1_V   IN     CAMBIO.ID_MONEDA_1%TYPE,
                          ID_MONEDA_2_V   IN     CAMBIO.ID_MONEDA_2%TYPE,
                          TIPO_CAMBIO_V   IN     CAMBIO.TIPO_CAMBIO%TYPE,
                          FECHA_V         IN     CAMBIO.FECHA%TYPE)
    AS
    BEGIN
        OUT_CAMBIO := DIENTES.CAMBIO_SQ.NEXTVAL;

        INSERT INTO DIENTES.CAMBIO (ID_MONEDA_1,
                                    ID_MONEDA_2,
                                    TIPO_CAMBIO,
                                    FECHA,
                                    ID_CAMBIO)
             VALUES (ID_MONEDA_1_V,
                     ID_MONEDA_2_V,
                     TIPO_CAMBIO_V,
                     FECHA_V,
                     OUT_CAMBIO);
    END ADD_CAMBIO;

    PROCEDURE ADD_CITA (OUT_CITA           OUT NUMBER,
                        ID_PACIENTE_V   IN     DIENTES.CITA.ID_PACIENTE%TYPE,
                        ID_DENTISTA_V   IN     DIENTES.CITA.ID_DENTISTA%TYPE,
                        FECHA_HORA_V    IN     varchar2,
                        DETALLE_V       IN     DIENTES.CITA.DETALLE%TYPE,
                        ASISTIO_V       IN     DIENTES.CITA.ASISTIO%TYPE,
                        ACEPTADA_V      IN     DIENTES.CITA.ACEPTADA%TYPE)
    IS
        FECHA Date;
    BEGIN
        OUT_CITA := DIENTES.CITA_SQ.NEXTVAL;
        
        FECHA := to_date(FECHA_HORA_V, 'MM/DD/YYYY HH:MI AM');

        INSERT INTO DIENTES.CITA (ID_CITA,
                                  ID_PACIENTE,
                                  ID_DENTISTA,
                                  FECHA_HORA,
                                  DETALLE,
                                  ASISTIO,
                                  ACEPTADA)
             VALUES (OUT_CITA,
                     ID_PACIENTE_V,
                     ID_DENTISTA_V,
                     FECHA,
                     DETALLE_V,
                     ASISTIO_V,
                     ACEPTADA_V);
    END ADD_CITA;

    PROCEDURE ADD_DETALLE_CITA (
        OUT_DETALLE_CITA              OUT NUMBER,
        ID_CITA_V                  IN     DIENTES.DETALLE_CITA.ID_CITA%TYPE,
        ID_TRATAMIENTOPACIENTE_V   IN     DIENTES.DETALLE_CITA.ID_TRATAMIENTOPACIENTE%TYPE)
    AS
    BEGIN
        OUT_DETALLE_CITA := DIENTES.DETALLECITA_SQ.NEXTVAL;

        INSERT
          INTO DIENTES.DETALLE_CITA (ID_DETALLE_CITA,
                                     ID_CITA,
                                     ID_TRATAMIENTOPACIENTE)
        VALUES (OUT_DETALLE_CITA, ID_CITA_V, ID_TRATAMIENTOPACIENTE_V);
    END ADD_DETALLE_CITA;

    PROCEDURE ADD_DIRECCION (
        OUT_DIRECCION      OUT NUMBER,
        ID_CIUDAD_V     IN     DIENTES.DIRECCIONES.ID_CIUDAD%TYPE,
        CALLE_V         IN     DIENTES.DIRECCIONES.CALLE%TYPE,
        NUMERO_V        IN     DIENTES.DIRECCIONES.NUMERO%TYPE,
        INFO_EXTRA_V    IN     DIENTES.DIRECCIONES.INFO_EXTRA%TYPE)
    AS
    BEGIN
        OUT_DIRECCION := DIENTES.DIRECCIONES_SQ.NEXTVAL;

        INSERT INTO DIENTES.DIRECCIONES (ID_DIRECCION,
                                         ID_CIUDAD,
                                         CALLE,
                                         NUMERO,
                                         INFO_EXTRA)
             VALUES (OUT_DIRECCION,
                     ID_CIUDAD_V,
                     CALLE_V,
                     NUMERO_V,
                     INFO_EXTRA_V);
    END ADD_DIRECCION;

    PROCEDURE ADD_ENFERMEDAD (
        OUT_ENFERMEDAD      OUT NUMBER,
        NOMBRE_V         IN     DIENTES.ENFERMEDADES.NOMBRE%TYPE)
    AS
    BEGIN
        OUT_ENFERMEDAD := DIENTES.ENFERMEDADES_SQ.NEXTVAL;

        INSERT INTO DIENTES.ENFERMEDADES (ID_ENFERMEDAD, NOMBRE)
             VALUES (OUT_ENFERMEDAD, NOMBRE_V);
    END ADD_ENFERMEDAD;

    PROCEDURE ADD_ESPECIALIDAD (
        OUT_ESPECIALIDAD      OUT NUMBER,
        NOMBRE_V           IN     DIENTES.ENFERMEDADES.NOMBRE%TYPE)
    AS
    BEGIN
        OUT_ESPECIALIDAD := DIENTES.ESPECIALIDADES_SQ.NEXTVAL;

        INSERT INTO DIENTES.ESPECIALIDADES (ID_ESPECIALIDAD, NOMBRE)
             VALUES (OUT_ESPECIALIDAD, NOMBRE_V);
    END ADD_ESPECIALIDAD;

    PROCEDURE ADD_ESPECIALIDAD_DENTISTA (
        ID_ESPECIALIDAD_V   IN DIENTES.ESPECIALIDAD_DENTISTA.ID_ESPECIALIDAD%TYPE,
        ID_DENTISTA_V       IN DIENTES.ESPECIALIDAD_DENTISTA.ID_DENTISTA%TYPE)
    AS
    BEGIN
        INSERT
          INTO DIENTES.ESPECIALIDAD_DENTISTA (ID_ESPECIALIDAD, ID_DENTISTA)
        VALUES (ID_ESPECIALIDAD_V, ID_DENTISTA_V);
    END ADD_ESPECIALIDAD_DENTISTA;

    PROCEDURE ADD_HORARIO (OUT_HORARIO      OUT NUMBER,
                            USUARIO_ID IN NUMBER,
                           LUNES_V       IN     VARCHAR2,
                           MARTES_V      IN     VARCHAR2,
                           MIERCOLES_V   IN     VARCHAR2,
                           JUEVES_V      IN     VARCHAR2,
                           VIERNES_V     IN     VARCHAR2,
                           SABADO_V      IN     VARCHAR2,
                           DOMINGO_V     IN     VARCHAR2)
    AS
    BEGIN
        OUT_HORARIO := DIENTES.HORARIO_SQ.NEXTVAL;

        INSERT INTO DIENTES.HORARIOS (ID_HORARIO,
                                      LUNES,
                                      MARTES,
                                      MIERCOLES,
                                      JUEVES,
                                      VIERNES,
                                      SABADO,
                                      DOMINGO)
             VALUES (OUT_HORARIO,
                     LUNES_V,
                     MARTES_V,
                     MIERCOLES_V,
                     JUEVES_V,
                     VIERNES_V,
                     SABADO_V,
                     DOMINGO_V);
         UPDATE DIENTES.USUARIOS USUARIO SET USUARIO.HORARIO = OUT_HORARIO WHERE USUARIO.ID_USUARIO = USUARIO_ID;
    END ADD_HORARIO;

    PROCEDURE ADD_MATERIAL (OUT_MATERIAL OUT INTEGER, NOMBRE_V IN VARCHAR2)
    AS
    BEGIN
        OUT_MATERIAL := DIENTES.MATERIAL_SQ.NEXTVAL;

        INSERT INTO DIENTES.MATERIAL (ID_MATERIAL, NOMBRE)
             VALUES (OUT_MATERIAL, NOMBRE_V);
    END ADD_MATERIAL;

    PROCEDURE ADD_PACIENTE_ALERGIA (ID_PACIENTE_V   IN INTEGER,
                                    ID_ALERGIA_V    IN INTEGER)
    AS
    BEGIN
        INSERT INTO DIENTES.PACIENTE_ALERGIA (ID_PACIENTE, ID_ALERGIA)
             VALUES (ID_PACIENTE_V, ID_ALERGIA_V);
    END ADD_PACIENTE_ALERGIA;

    PROCEDURE ADD_PACIENTE_ENFERMEDAD (ID_PACIENTE_V     IN INTEGER,
                                       ID_ENFERMEDAD_V   IN INTEGER)
    AS
    BEGIN
        INSERT INTO DIENTES.PACIENTE_ENFERMEDAD (ID_PACIENTE, ID_ENFERMEDAD)
             VALUES (ID_PACIENTE_V, ID_ENFERMEDAD_V);
    END ADD_PACIENTE_ENFERMEDAD;

    PROCEDURE ADD_PAGOS (
        OUT_PAGO            OUT DIENTES.PAGOS.ID_PAGO%TYPE,
        ID_DENTISTA_V    IN     DIENTES.PAGOS.ID_DENTISTA%TYPE,
        ID_PACIENTE_V    IN     DIENTES.PAGOS.ID_PACIENTE%TYPE,
        FECHA_V          IN     DIENTES.PAGOS.FECHA%TYPE,
        TOTAL_V          IN     DIENTES.PAGOS.TOTAL%TYPE,
        ID_TIPOPAGOS_V   IN     DIENTES.PAGOS.ID_TIPOPAGOS%TYPE,
        ID_CAMBIO_V      IN     DIENTES.PAGOS.ID_CAMBIO%TYPE)
    AS
    BEGIN
        OUT_PAGO := DIENTES.PAGOS_SQ.NEXTVAL;

        INSERT INTO DIENTES.PAGOS (ID_PAGO,
                                   ID_DENTISTA,
                                   ID_PACIENTE,
                                   FECHA,
                                   TOTAL,
                                   ID_TIPOPAGOS,
                                   ID_CAMBIO)
             VALUES (OUT_PAGO,
                     ID_DENTISTA_V,
                     ID_PACIENTE_V,
                     FECHA_V,
                     TOTAL_V,
                     ID_TIPOPAGOS_V,
                     ID_CAMBIO_V);
    END ADD_PAGOS;
    
    PROCEDURE ADD_TIPO_PAGO(OUT_TIPOPAGOS OUT INTEGER, NOMBRE_V IN VARCHAR2)
    AS
    BEGIN
    OUT_TIPOPAGOS := DIENTES.TIPOPAGOS_SQ.NEXTVAL;
    INSERT INTO DIENTES.TIPO_PAGOS (
   ID_TIPOPAGOS, NOMBRE) 
VALUES ( OUT_TIPOPAGOS,NOMBRE_V);
    END ADD_TIPO_PAGO;
    
    PROCEDURE ADD_TIPO_SANGRE(OUT_TIPOSANGRE OUT INTEGER, NOMBRE_V IN VARCHAR2)
    AS
    BEGIN
    OUT_TIPOSANGRE := DIENTES.TIPO_SANGRE_SQ.NEXTVAL;
    INSERT INTO DIENTES.TIPO_SANGRE (
   ID_TIPO_SANGRE, NOMBRE) 
VALUES ( OUT_TIPOSANGRE,NOMBRE_V);
    END ADD_TIPO_SANGRE;
    
    PROCEDURE ADD_TRATAMIENTO (OUT_TRATAMIENTO OUT INTEGER, NOMBRE_V IN VARCHAR2, COSTO_V IN LONG, ID_ESPECIALIDAD_V IN INTEGER)
    AS
    BEGIN 
    OUT_TRATAMIENTO := DIENTES.TRATAMIENTO_SQ.NEXTVAL;
    INSERT INTO DIENTES.TRATAMIENTO (
   ID_TRATAMIENTO, NOMBRE, COSTO, 
   ID_ESPECIALIDAD) 
VALUES (OUT_TRATAMIENTO, NOMBRE_V, COSTO_V, ID_ESPECIALIDAD_V);
    END ADD_TRATAMIENTO;
    
    PROCEDURE ADD_TRATAMIENTO_MATERIAL(ID_TRATAMIENTO_V IN INTEGER, ID_MATERIAL_V IN INTEGER)
    AS
    BEGIN
    INSERT INTO DIENTES.TRATAMIENTO_MATERIAL (
   ID_TRATAMIENTO, ID_MATERIAL) 
VALUES (ID_TRATAMIENTO_V, ID_MATERIAL_V);
    END ADD_TRATAMIENTO_MATERIAL;
    
    /* Formatted on 5/21/2017 9:17:47 PM (QP5 v5.300) */
PROCEDURE ADD_TRATAMIENTO_PACIENTE (OUT_TRATAMIENTOPACIENTE      OUT INTEGER,
                                    ID_TRATAMIENTO_V          IN     INTEGER,
                                    ID_PACIENTE_V             IN     INTEGER,
                                    COSTO_V                   IN     LONG,
                                    CITAS_NUMERO_V            IN     INTEGER,
                                    CITAS_TOTAL_V             IN     INTEGER,
                                    ABONOS_TOTALES_V          IN     INTEGER)
    AS
    BEGIN
    INSERT INTO DIENTES.TRATAMIENTO_PACIENTE (
   ID_TRATAMIENTOPACIENTE, ID_TRATAMIENTO, ID_PACIENTE, 
   COSTO, CITAS_NUMERO, CITAS_TOTAL, 
   ABONOS_TOTALES) 
VALUES ( OUT_TRATAMIENTOPACIENTE, ID_TRATAMIENTO_V, ID_PACIENTE_V, 
   COSTO_V, CITAS_NUMERO_V, CITAS_TOTAL_V, 
   ABONOS_TOTALES_V);
    END ADD_TRATAMIENTO_PACIENTE;
END ADD_PKG;
/