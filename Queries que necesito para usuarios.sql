CREATE OR REPLACE procedure DIENTES.get_country(pais out sys_refcursor)
as
begin
    open pais for
        Select paises.id_pais, paises.nombre from DIENTES.PAISES paises order by paises.id_pais asc;
end;

create or replace procedure dientes.get_estados(pais in integer, estados out sys_refcursor)
as
begin
    open estados for
        Select estados.id_estado, estados.NOMBRE from DIENTES.ESTADO estados where estados.ID_PAIS = pais order by estados.NOMBRE asc;
end;

create or replace procedure dientes.get_ciudades(states in integer, ciudad out sys_refcursor)
as
begin
    open ciudad for
        Select city.ID_CIUDAD, city.NOMBRE from DIENTES.CIUDADES city where city.ID_ESTADO = states order by city.nombre asc;
end;

create or replace procedure dientes.creardireccion(usuario in integer, celular in integer, ciudad in integer, interior in integer, calle in varchar2, sexo in varchar2)
is
id_direccion integer;
begin
id_direccion:= DIENTES.DIRECCIONES_SQ.nextval;
insert into dientes.direcciones dir (dir.ID_DIRECCION, dir.CALLE, dir.NUMERO, dir.ID_CIUDAD) values (id_direccion, calle, interior, ciudad);
insert into dientes.usuarios usuario (usuario.ID_USUARIO, usuario.ID_DIRECCION, usuario.SEXO, usuario.CELULAR) values (usuario, id_direccion, sexo, celular);
end;

create or replace procedure dientes.getuserinfo(usuario in integer, informacion out sys_refcursor)
as
begin
    open informacion for
        select mainusuario.FIRST_NAME, mainusuario.LAST_NAME, mainusuario.EMAIL, direccion.CALLE, direccion.NUMERO, direccion.ID_CIUDAD, ciudad.ID_ESTADO,
        estados.ID_PAIS, secondusuario.CELULAR, secondusuario.SEXO
        from dientes.auth_user mainusuario inner join DIENTES.USUARIOS secondusuario on mainusuario.ID=secondusuario.ID_USUARIO 
        inner join DIENTES.DIRECCIONES direccion on secondusuario.ID_DIRECCION = direccion.ID_DIRECCION inner join DIENTES.CIUDADES ciudad
        on direccion.ID_CIUDAD = ciudad.ID_CIUDAD inner join DIENTES.ESTADO estados on ciudad.ID_ESTADO = estados.ID_ESTADO
        where mainusuario.ID = usuario;
end;

variable rc refcursor;
exec DIENTES.GET_ciudades(37, :rc);
print rc;

Select estados.id_estado, estados.NOMBRE from DIENTES.ESTADO estados where estados.ID_PAIS = 142;

select mainusuario.FIRST_NAME, mainusuario.LAST_NAME, mainusuario.EMAIL, direccion.CALLE, direccion.NUMERO, direccion.ID_CIUDAD, ciudad.ID_ESTADO,
        estados.ID_PAIS, secondusuario.CELULAR, secondusuario.SEXO
        from dientes.auth_user mainusuario inner join DIENTES.USUARIOS secondusuario on mainusuario.ID=secondusuario.ID_USUARIO 
        inner join DIENTES.DIRECCIONES direccion on secondusuario.ID_DIRECCION = direccion.ID_DIRECCION inner join DIENTES.CIUDADES ciudad
        on direccion.ID_CIUDAD = ciudad.ID_CIUDAD inner join DIENTES.ESTADO estados on ciudad.ID_ESTADO = estados.ID_ESTADO
        where mainusuario.ID = 1;
        

create or replace procedure dientes.actualizardireccion(usuario in integer, nombre in varchar2, apellido in varchar2, correo in varchar2, 
cell in integer, ciudad in integer, interior in integer, street in varchar2, sex in varchar2)
is
id_dir integer;
begin
select DIENTES.USUARIOS.ID_DIRECCION into id_dir from DIENTES.USUARIOS where DIENTES.USUARIOS.ID_USUARIO = usuario;
update DIENTES.DIRECCIONES dir set dir.CALLE = street, dir.NUMERO = interior, dir.ID_CIUDAD = ciudad where dir.ID_DIRECCION = id_dir;
update dientes.auth_user primario set primario.FIRST_NAME = nombre, primario.LAST_NAME=apellido, primario.EMAIL=correo where primario.ID = usuario;
update dientes.usuarios secundario set secundario.ID_DIRECCION=id_dir, secundario.SEXO=sex, secundario.CELULAR=cell where secundario.ID_USUARIO = usuario;
end;
        

begin
dientes.actualizardireccion(1, 'test2', 'test2', 'test2', 12345, 22, 789, 'test2', 'T');
end;

update dientes.direcciones dir set dir.CALLE='test', dir.NUMERO=123, dir.ID_CIUDAD=20 where dir.ID_DIRECCION=6;

update dientes.usuarios secundario set secundario.ID_DIRECCION=9, secundario.SEXO='U', secundario.CELULAR=123 where secundario.ID_USUARIO = 1;
