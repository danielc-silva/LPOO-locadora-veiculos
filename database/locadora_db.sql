-- Nota: Execute este comando separadamente se estiver usando um gerenciador como pgAdmin ou DBeaver
-- criar o DATABASE db_lpoo_locadora_veiculos;

CREATE TABLE tb_veiculos (
    vei_id SERIAL PRIMARY KEY,
    vei_placa CHAR(7) UNIQUE NOT NULL,
    vei_categoria VARCHAR(20) NOT NULL,
    vei_taxa_diaria NUMERIC(10,2) NOT NULL,
    vei_estado_atual VARCHAR(20),
    vei_tipo VARCHAR(20) NOT NULL
);

CREATE TABLE tb_locacoes (
    loc_id SERIAL PRIMARY KEY,
    vei_placa CHAR(7) NOT NULL,
    loc_data_inicio DATE NOT NULL,
    loc_data_fim DATE NOT NULL,
    loc_status VARCHAR(20) NOT NULL,
    loc_valor_total NUMERIC(10, 2),
    loc_estrategia VARCHAR(100) NOT NULL DEFAULT 'PADRAO',
    
    CONSTRAINT fk_veiculo
        FOREIGN KEY (vei_placa) 
        REFERENCES tb_veiculos(vei_placa)
        ON DELETE RESTRICT
);