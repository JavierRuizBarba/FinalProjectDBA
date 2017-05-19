/* Formatted on 5/17/2017 1:32:14 PM (QP5 v5.300) */
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
END ADD_PKG;