# User-Management-Application
Esta aplicação é um sistema CRUD para gerenciamento de usuários, desenvolvido em Python com Tkinter e SQLite. Organizado conforme o padrão MVC e com programação orientada a objetos, permite cadastrar, ler, atualizar e excluir registros, além de exportar dados para CSV.

# User Management Application

Essa aplicação é um exemplo de sistema de gerenciamento de usuários desenvolvido com **Python**, **Tkinter** e **SQLite**. O projeto foi estruturado utilizando o padrão **MVC (Model-View-Controller)** com programação orientada a objetos, demonstrando uma organização modular e escalável para aplicações desktop.

---

## Visão Geral

- **Model (UsuarioModel):**  
  - Gerencia a conexão com o banco de dados `users.db` (SQLite).
  - Cria a tabela `usuarios` se ela não existir.
  - Realiza operações de cadastro e atualização dos dados dos usuários.

- **View (UsuarioView):**  
  - Gerencia a interface gráfica utilizando Tkinter.
  - Fornece telas para login, cadastro (usuário comum e administrador), painel do usuário e painel de administração.
  - Cada tela mantém o layout e a lógica original, com funcionalidades para alterar senha/email, exportar dados para CSV e deletar usuários.

- **Controller (UsuarioController):**  
  - Integra o Model e a View.
  - Inicia a aplicação criando o banco de dados e direcionando o fluxo para a tela de login.

---

## Funcionalidades

- **Cadastro de Usuários:**  
  Permite o registro de usuários comuns e administradores, com validação dos campos (nome, email e senha).

![Image](https://github.com/user-attachments/assets/35ec83f7-6a22-4b5e-8721-4c0600c78d41)

- **Login:**  
  Verifica as credenciais inseridas e redireciona:
  - **Administradores** para o painel de administração.
  - **Usuários comuns** para o painel do usuário.
  
  ![Image](https://github.com/user-attachments/assets/b1e41ba2-def5-4753-a44c-28b961c9e28a)

- **Painel do Usuário:**  
  Exibe as informações pessoais do usuário, possibilitando a alteração de senha e/ou email.

![Image](https://github.com/user-attachments/assets/bd53fb0e-aeb3-4766-bbd3-21f43ec6d0ff)
  

- **Painel de Administração:**  
  Permite ao administrador gerenciar usuários:
  - Busca e listagem de usuários.
  - Alteração de senha.
  - Deleção de registros.
  - Exportação dos dados para um arquivo CSV (`usuarios_exportados.csv`).

- **Exportação para CSV:**  
  Gera um arquivo CSV contendo os dados dos usuários, facilitando análises ou backups.

![Image](https://github.com/user-attachments/assets/8beea34e-521d-4632-a043-2fe00d4499bc)

---

## Requisitos

- **Python 3.x**  
  Certifique-se de ter o Python 3 instalado.

- **Tkinter**  
  Biblioteca padrão para interfaces gráficas (geralmente incluída na instalação do Python).

- **SQLite3**  
  Módulo para gerenciamento do banco de dados local (incluído com o Python).

- **CSV**  
  Módulo padrão para manipulação e exportação de dados em formato CSV.

---

## Como Executar

1. **Abra o executavel:**
