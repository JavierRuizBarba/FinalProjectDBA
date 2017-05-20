select * from DIENTES.Estado estados inner join DIENTES.CIUDADES ciudades on estados.ID_ESTADO = ciudades.ID_ESTADO;

create or replace procedure dientes.get_country(pais out sys_refcursor)
as
begin
    open pais for
        Select paises.id_pais, paises.nombre from DIENTES.PAISES paises;
end;

create or replace procedure dientes.get_estados(pais in integer, estados out sys_refcursor)
as
begin
    open get_estados for
        Select DIENTES.ESTADO.ID_ESTADO, dientes.estado.nombre from DIENTES.ESTADO estados where estados.ID_PAIS = pais;
end;