-- =====================================================================
-- Sistema de Estoque e Atendimento - criação do banco e das tabelas (DDL)
-- Requer MySQL 8.0.16 ou mais novo (a partir dessa versão o CHECK é aplicado)
-- Pode ser executado mais de uma vez: não apaga nada que já exista.
-- Dados de exemplo: rode database/seed.sql depois deste script.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS estoque_atendimento CHARACTER SET utf8mb4;
USE estoque_atendimento;

-- Lojista: quem opera o sistema. PK = login
-- A senha é guardada em forma de HASH (SHA2 = 64 caracteres), para que as senhas não fiquem visíveis
CREATE TABLE IF NOT EXISTS lojista (
    login     VARCHAR(30)  PRIMARY KEY,
    cpf       CHAR(11)     NOT NULL UNIQUE,
    prenome   VARCHAR(50)  NOT NULL,
    sobrenome VARCHAR(100) NOT NULL,
    senha     VARCHAR(255) NOT NULL,
    funcao    VARCHAR(50)  NOT NULL
);

-- Mercadoria: catálogo do estoque. PK = referência
-- DECIMAL(10,2) para dinheiro: FLOAT gera erros de arredondamento
CREATE TABLE IF NOT EXISTS mercadoria (
    referencia    VARCHAR(20)   PRIMARY KEY,
    nome          VARCHAR(100)  NOT NULL,
    quantidade    INT           NOT NULL DEFAULT 0,
    preco         DECIMAL(10,2) NOT NULL,
    login_lojista VARCHAR(30)   NOT NULL,   -- relacionamento "Gerencia" (1:N)

    INDEX idx_mercadoria_nome (nome),

    CONSTRAINT ck_mercadoria_quantidade CHECK (quantidade >= 0),
    CONSTRAINT ck_mercadoria_preco      CHECK (preco >= 0),

    CONSTRAINT fk_mercadoria_lojista
        FOREIGN KEY (login_lojista) REFERENCES lojista(login)
        ON DELETE RESTRICT   -- não apaga lojista que ainda gerencia mercadorias
        ON UPDATE CASCADE
);

-- Cliente: nome composto vira duas colunas (prenome + sobrenome)
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT          PRIMARY KEY AUTO_INCREMENT,
    cpf        CHAR(11)     NOT NULL UNIQUE,
    prenome    VARCHAR(50)  NOT NULL,
    sobrenome  VARCHAR(100) NOT NULL
);

-- Telefone é multivalorado -> tabela própria (1FN): um cliente pode ter vários telefones
CREATE TABLE IF NOT EXISTS telefone_cliente (
    id_telefone INT         PRIMARY KEY AUTO_INCREMENT,
    id_cliente  INT         NOT NULL,
    telefone    VARCHAR(15) NOT NULL,

    CONSTRAINT uq_telefone_cliente UNIQUE (id_cliente, telefone),

    CONSTRAINT fk_telefone_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        ON DELETE CASCADE    -- apagou o cliente, apaga os telefones dele
        ON UPDATE CASCADE
);

-- Atendimento: cada entrada na fila. servico_prestado fica NULL enquanto o cliente espera
CREATE TABLE IF NOT EXISTS atendimento (
    id_atendimento     INT          PRIMARY KEY AUTO_INCREMENT,
    ordem_fila         INT          NOT NULL,   -- posição de chegada (regra FIFO)
    servico_solicitado VARCHAR(100) NOT NULL,
    servico_prestado   VARCHAR(100) NULL,
    id_cliente         INT          NOT NULL,   -- relacionamento "Entra" (1:N)
    login_lojista      VARCHAR(30)  NOT NULL,   -- relacionamento "Processa" (1:N)

    INDEX idx_atendimento_ordem (ordem_fila),

    CONSTRAINT ck_atendimento_ordem CHECK (ordem_fila > 0),

    CONSTRAINT fk_atendimento_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        ON DELETE RESTRICT   -- não apaga cliente que tem atendimentos
        ON UPDATE CASCADE,

    CONSTRAINT fk_atendimento_lojista
        FOREIGN KEY (login_lojista) REFERENCES lojista(login)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabela associativa do N:N "Utiliza" (Atendimento <-> Mercadoria)
-- PK composta: a mesma mercadoria não repete no mesmo atendimento
CREATE TABLE IF NOT EXISTS item_atendimento (
    id_atendimento       INT         NOT NULL,
    referencia           VARCHAR(20) NOT NULL,
    quantidade_utilizada INT         NOT NULL,

    PRIMARY KEY (id_atendimento, referencia),

    CONSTRAINT ck_item_quantidade CHECK (quantidade_utilizada > 0),

    CONSTRAINT fk_item_atendimento
        FOREIGN KEY (id_atendimento) REFERENCES atendimento(id_atendimento)
        ON DELETE CASCADE    -- apagou o atendimento, apaga os itens dele
        ON UPDATE CASCADE,

    CONSTRAINT fk_item_mercadoria
        FOREIGN KEY (referencia) REFERENCES mercadoria(referencia)
        ON DELETE RESTRICT   -- não apaga mercadoria que já foi usada em atendimento
        ON UPDATE CASCADE
);
