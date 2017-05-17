ALTER TABLE DIENTES.CITA
DROP CONSTRAINT CITA_R01;

ALTER TABLE DIENTES.CITA
DROP CONSTRAINT CITA_R02;

ALTER TABLE DIENTES.CITA ADD (
  CONSTRAINT CITA_R01 
  FOREIGN KEY (ID_DENTISTA) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE,
  CONSTRAINT CITA_R02 
  FOREIGN KEY (ID_PACIENTE) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE);

ALTER TABLE DIENTES.ESPECIALIDAD_DENTISTA
DROP CONSTRAINT ESPECIALIDAD_DENTISTA_R02;

ALTER TABLE DIENTES.ESPECIALIDAD_DENTISTA ADD (
  CONSTRAINT ESPECIALIDAD_DENTISTA_R02 
  FOREIGN KEY (ID_DENTISTA) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE);

ALTER TABLE DIENTES.PACIENTE_ALERGIA
DROP CONSTRAINT PACIENTE_ALERGIA_R01;

ALTER TABLE DIENTES.PACIENTE_ALERGIA ADD (
  CONSTRAINT PACIENTE_ALERGIA_R01 
  FOREIGN KEY (ID_PACIENTE) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE);


ALTER TABLE DIENTES.PACIENTE_ENFERMEDAD
DROP CONSTRAINT PACIENTE_ENFERMEDAD_R01;

ALTER TABLE DIENTES.PACIENTE_ENFERMEDAD ADD (
  CONSTRAINT PACIENTE_ENFERMEDAD_R01 
  FOREIGN KEY (ID_PACIENTE) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE);

ALTER TABLE DIENTES.PAGOS
DROP CONSTRAINT PAGOS_R01;

ALTER TABLE DIENTES.PAGOS
DROP CONSTRAINT PAGOS_R02;

ALTER TABLE DIENTES.PAGOS ADD (
  CONSTRAINT PAGOS_R01 
  FOREIGN KEY (ID_PACIENTE) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE,
  CONSTRAINT PAGOS_R02 
  FOREIGN KEY (ID_PACIENTE) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE);

ALTER TABLE DIENTES.TRATAMIENTO_PACIENTE
DROP CONSTRAINT TRATAMIENTO_PACIENTE_R02;

ALTER TABLE DIENTES.TRATAMIENTO_PACIENTE ADD (
  CONSTRAINT TRATAMIENTO_PACIENTE_R02 
  FOREIGN KEY (ID_PACIENTE) 
  REFERENCES DIENTES.USUARIOS (ID_USUARIO)
  ENABLE VALIDATE);

DROP TABLE DIENTES.PACIENTES;
DROP TABLE DIENTES.DENTISTAS;

ALTER TABLE DIENTES.USUARIOS
  ADD (horario number,
       contacto varchar2(40),
       tipo_sangre number);
       
CREATE TABLE DIENTES.TIPO_SANGRE
(
  ID_TIPO_SANGRE  NUMBER                        NOT NULL,
  NOMBRE          VARCHAR2(4)
);


ALTER TABLE DIENTES.TIPO_SANGRE ADD (
  CONSTRAINT TIPO_SANGRE_PK
  PRIMARY KEY
  (ID_TIPO_SANGRE)
  ENABLE VALIDATE);
  
ALTER TABLE DIENTES.USUARIOS ADD 
CONSTRAINT USUARIOS_R01
 FOREIGN KEY (TIPO_SANGRE)
 REFERENCES DIENTES.TIPO_SANGRE (ID_TIPO_SANGRE)
 ENABLE
 VALIDATE;
 
 
 ALTER TABLE DIENTES.HORARIOS
 DROP PRIMARY KEY CASCADE;

DROP TABLE DIENTES.HORARIOS CASCADE CONSTRAINTS;

CREATE TABLE DIENTES.HORARIOS
(
  ID_HORARIO  NUMBER                            NOT NULL,
  LUNES       VARCHAR2(40 BYTE),
  MARTES      VARCHAR2(40 BYTE),
  MIERCOLES   VARCHAR2(40 BYTE),
  JUEVES      VARCHAR2(40 BYTE),
  VIERNES     VARCHAR2(40 BYTE),
  SABADO      VARCHAR2(40 BYTE),
  DOMINGO     VARCHAR2(40 BYTE)
)
TABLESPACE SYSTEM
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
MONITORING;


CREATE UNIQUE INDEX DIENTES.HORARIOS_PK ON DIENTES.HORARIOS
(ID_HORARIO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
           );

ALTER TABLE DIENTES.HORARIOS ADD (
  CONSTRAINT HORARIOS_PK
  PRIMARY KEY
  (ID_HORARIO)
  USING INDEX DIENTES.HORARIOS_PK
  ENABLE VALIDATE);

ALTER TABLE DIENTES.USUARIOS ADD 
CONSTRAINT USUARIOS_R02
 FOREIGN KEY (HORARIO)
 REFERENCES DIENTES.HORARIOS (ID_HORARIO)
 ENABLE
 VALIDATE;
 
CREATE SEQUENCE DIENTES.TIPO_SANGRE_SQ
START WITH 0
INCREMENT BY 1
MINVALUE 0
NOCACHE 
NOCYCLE 
NOORDER;

CREATE SEQUENCE DIENTES.HORARIO_SQ
START WITH 0
INCREMENT BY 1
MINVALUE 0
NOCACHE 
NOCYCLE 
NOORDER;
