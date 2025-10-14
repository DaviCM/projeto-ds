use u275872813_controle_gasto;
create table tb_usuario_davicoelho(
	-- a melhor tabela da história --
    
    id int primary key auto_increment,
    nome varchar(120) not null,
    email varchar(120) unique,
    senha varchar(255)
);


