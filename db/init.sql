CREATE DATABASE clientes;

\c clientes;

Create Table clientes(
	id serial primary key,
	Nome varchar(100) not null,
	Documento varchar(100) not null,
	Ativo bool default true
);


Create Table enderecos(
	id serial primary key,
	logradouro varchar(250) not null,
	bairro varchar(100) not null,
	cep varchar(100) not null,
	numero varchar(10) not null,
	complemento varchar(250) null,
	cidade varchar(100) not null,
	estado varchar(50) not null,
	idCliente int not null,
	Ativa bool default true,
	foreign key (idCliente) references clientes(id)
);