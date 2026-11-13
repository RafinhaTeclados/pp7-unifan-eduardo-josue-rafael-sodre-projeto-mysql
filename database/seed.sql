-- =====================================================================
-- Dados de exemplo (DML). Rode DEPOIS do banco.sql.
-- ATENÇÃO: este script APAGA os dados atuais das tabelas e recria os exemplos,
-- então pode ser executado quantas vezes quiser (útil antes da apresentação).
-- =====================================================================

USE estoque_atendimento;

-- Limpa as tabelas (FOREIGN_KEY_CHECKS desligado só durante a limpeza)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE item_atendimento;
TRUNCATE TABLE atendimento;
TRUNCATE TABLE telefone_cliente;
TRUNCATE TABLE cliente;
TRUNCATE TABLE mercadoria;
TRUNCATE TABLE lojista;
SET FOREIGN_KEY_CHECKS = 1;

-- Senhas de exemplo guardadas como hash (SHA2 de 256 bits)
INSERT INTO lojista (login, cpf, prenome, sobrenome, senha, funcao) VALUES
('eduardo', '98765432100', 'Eduardo', 'de Lima',  SHA2('teste123', 256), 'Gerente'),
('rafael',  '98765432101', 'Rafael',  'Sodré', SHA2('teste456', 256), 'Atendente'),
('josue', '98765432102', 'Josué', 'Calebe',   SHA2('teste789', 256), 'Atendente');

INSERT INTO mercadoria (referencia, nome, quantidade, preco, login_lojista) VALUES
('MOU-001', 'Mouse',           10,  80.00, 'eduardo'),
('TEC-001', 'Teclado',          5, 120.00, 'eduardo'),
('WEB-001', 'Webcam',           4, 200.00, 'eduardo'),
('MON-001', 'Monitor',          3, 900.00, 'rafael'),
('CAB-001', 'Cabo USB',        20,  25.00, 'rafael'),
('PEN-001', 'Pen drive 32GB',  30,  40.00, 'rafael'),
('HDM-001', 'Cabo HDMI',       15,  35.00, 'josue'),
('FON-001', 'Fone de ouvido',   8, 150.00, 'josue');

INSERT INTO cliente (cpf, prenome, sobrenome) VALUES
('12345678901', 'Ana',    'Souza'),
('12345678902', 'Carlos', 'Pereira'),
('12345678903', 'Maria',  'Oliveira'),
('12345678904', 'José',   'Ribeiro'),
('12345678905', 'Paula',  'Costa'),
('12345678906', 'Rafael', 'Mendes');   -- ainda sem atendimento

INSERT INTO telefone_cliente (id_cliente, telefone) VALUES
(1, '71999999999'), (1, '7433334444'),
(2, '71988888888'),
(3, '71977777777'),
(4, '71966666666'), (4, '7432221111'),
(5, '71955555555'),
(6, '71944444444');

-- Atendimentos 1 a 4 já concluídos; 5, 6 e 7 ainda estão na fila (servico_prestado NULL)
INSERT INTO atendimento (ordem_fila, servico_solicitado, servico_prestado, id_cliente, login_lojista) VALUES
(1, 'Compra de acessórios',     'Compra concluída', 1, 'rafael'),
(2, 'Troca de produto',         'Troca realizada',  2, 'rafael'),
(3, 'Compra de monitor',        'Compra concluída', 3, 'eduardo'),
(4, 'Compra de periféricos',    'Compra concluída', 1, 'josue'),
(5, 'Informação sobre produto', NULL,               4, 'rafael'),
(6, 'Ajuda com compra',         NULL,               5, 'josue'),
(7, 'Compra de fone',           NULL,               2, 'eduardo');

INSERT INTO item_atendimento (id_atendimento, referencia, quantidade_utilizada) VALUES
(1, 'MOU-001', 1), (1, 'CAB-001', 2),
(2, 'TEC-001', 1),
(3, 'MON-001', 1), (3, 'HDM-001', 1),
(4, 'HDM-001', 2), (4, 'PEN-001', 1), (4, 'FON-001', 1),
(6, 'WEB-001', 1),
(7, 'FON-001', 1);                    -- o atendimento 5 (só informação) não tem itens

-- Testes:
SELECT * FROM mercadoria;