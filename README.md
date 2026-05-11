# Sistema de Locadora de Veículos

O projeto é um sistema desktop criado para gerenciar uma locadora de veículos. A ideia central é ter uma Janela Principal com um menu que dá acesso às seguintes áreas:

* **Cadastro de Veículos:** Para gerenciar os carros da locadora.
* **Atendimento (Usuário):** Para registrar as locações do dia a dia, devoluções e cancelamentos.
* **Acesso Administrador:** Um painel com acesso irrestrito, onde o admin pode editar, excluir e alterar qualquer informação dentro das locações para corrigir dados.

O sistema foi feito em Python (Tkinter) e conectado a um banco de dados PostgreSQL.

---

## Detalhamento de Aprendizado

* **Dificuldades Encontradas:** Controlar a navegação das telas sem sobreposição no Tkinter e validar a disponibilidade dos veículos direto no banco de dados.
* **Como resolvi:** Realizei pesquisas em documentações e contei com o auxílio de IA para entender o controle de janelas e estruturar as consultas SQL.
* **Principal Aprendizado:** Aplicação prática da arquitetura MVC, integrando a interface gráfica com as regras de negócio no banco.

---

## Declaração de Uso de IA

- [ ] **Nenhuma IA foi utilizada** na elaboração deste código.
- [x] **Utilizei IA** como ferramenta de apoio.
- **Ferramenta:** Gemini 3.1 Pro.
- **Finalidade:** Me ajudou a ajustar a consulta SQL para filtrar os veículos disponíveis por data e a entender como fazer as janelas do Tkinter abrirem e fecharem sem bugar.
- **Validação:** Li, testei e adaptei todo o código gerado para que funcionasse perfeitamente com o banco de dados e as regras do meu projeto.