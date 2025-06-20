import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import csv

# MODEL: Gerencia os dados e a conexão com o banco
class UsuarioModel:
    def __init__(self):
        # Inicia a conexão com o banco ao criar a instância
        self.conectar()

    def conectar(self):
        # Estabelece a conexão com o banco "users.db" e cria um cursor
        self.conexao = sqlite3.connect("users.db")
        self.cursor = self.conexao.cursor()
        # Cria a tabela "usuarios" se ela não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL DEFAULT 'senha123',
                tipo TEXT NOT NULL DEFAULT 'usuario'
            )
        ''')
        self.conexao.commit()

    def cadastrar_usuario_bd(self, nome, email, senha, tipo='usuario'):
        # Tenta inserir um novo registro na tabela com os dados fornecidos
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha, tipo)
            )
            self.conexao.commit()
            # Mensagem de sucesso caso a inserção seja realizada
            messagebox.showinfo("Sucesso", f"Usuário {tipo} cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            # Caso haja violação da unicidade de algum campo
            messagebox.showerror("Erro", "Email ou nome já cadastrado.")
        except Exception as e:
            # Trata outras exceções e exibe o erro
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

    def fechar(self):
        # Fecha a conexão com o banco de dados
        self.conexao.close()


# VIEW: Gerencia a interface gráfica e a interação com o usuário
class UsuarioView:
    def __init__(self, model):
        self.model = model

    def centralizar_janela(self, janela, largura=400, altura=300):
        """Centraliza a janela na tela com a largura e altura fornecidas."""
        janela.update_idletasks()
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    # --- Validação dos dados de cadastro e chamada do método de cadastro no Model ---
    def verificar(self, entry_nome, entry_senha, entry_email, tipo='usuario'):
        # Obtém os valores dos campos
        nome = str(entry_nome.get())
        senha = entry_senha.get()
        email = entry_email.get()
        # Verifica se os campos foram preenchidos
        if nome and senha and email:
            # Verifica se o email contém exatamente um '@' e um ponto
            if email.count('@') != 1 or '.' not in email:
                messagebox.showerror("Erro", "Email inválido.")
                return
            # Verifica se a senha tem pelo menos 6 caracteres
            elif len(senha) < 6:
                messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres.")
                return
            # Verifica se o nome possui pelo menos 3 caracteres
            elif len(nome) < 3:
                messagebox.showerror("Erro", "O nome deve ter pelo menos 3 caracteres.")
                return
            # Se tudo estiver correto, chama o método de cadastro do Model
            self.model.cadastrar_usuario_bd(nome, email, senha, tipo)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # --- Tela de cadastro para usuários comuns ---
    def cadastrar_usuario(self,tipo='usuario'):
        print("Cadastrando usuário...")
        janela = tk.Tk()
        janela.title("Cadastro de Usuários")
        self.centralizar_janela(janela, 400, 300)
        tk.Label(janela, text="Usuário:").pack()
        entry_nome = tk.Entry(janela, width=40)
        entry_nome.pack()
        tk.Label(janela, text="email:").pack()
        entry_email = tk.Entry(janela, width=40)
        entry_email.pack()
        tk.Label(janela, text="Senha:").pack()
        entry_senha = tk.Entry(janela, width=40, show="*")
        entry_senha.pack()
        
        tk.Button(janela, text="Cadastrar Usuário", width=40, height=3, 
                  command=lambda: self.verificar(entry_nome, entry_senha, entry_email, tipo='usuario')
                 ).pack(pady=10)
        
        if tipo == 'admin':
            tk.Button(janela, text="Voltar", width=40, height=1, 
                  command=lambda: (janela.destroy(), self.tela_admin())
                 ).pack(pady=10)
            
        else:
            tk.Button(janela, text="Voltar", width=40, height=1, 
                    command=lambda: (janela.destroy(), self.tela_login())
                    ).pack(pady=10)
        
        tk.Button(janela, text="Sair", width=40, height=1, 
                  command=lambda: (janela.destroy(), self.fechar_programa())
                 ).pack(pady=10)
        
        if tipo == 'admin':
            tk.Button(janela, text="Cadastrar Usuário Admin", width=40, height=3,
                      command=lambda: (janela.destroy(), self.cadastrar_usuario_admin())
                     ).pack(pady=10)

    # --- Tela de fim: Fecha o programa ---
    def fechar_programa(self):
        if messagebox.askyesno("Sair", "Você tem certeza que deseja sair?"):
            self.model.fechar()
            exit()

    # --- Tela de login (início) ---
    def tela_login(self):
        # Reconecta ao banco (equivalente à função conectar_banco)
        self.model.conectar()
        janela = tk.Tk()
        janela.title("Login")
        tk.Label(janela, text="Usuário:").pack()
        entry_nome = tk.Entry(janela, width=40)
        entry_nome.pack()
        tk.Label(janela, text="Senha:").pack()
        entry_senha = tk.Entry(janela, width=40, show="*")
        entry_senha.pack()
        # Botão de login: chama o método login
        tk.Button(janela, text="Login", width=40, height=3,
                  command=lambda: self.login(entry_nome, entry_senha, janela)
                 ).pack(pady=10)
        # Botão para chamar tela de cadastro de usuário comum
        tk.Button(janela, text="Cadastrar Usuário", width=40, height=3, 
                  command=lambda: (janela.destroy(), self.cadastrar_usuario())
                 ).pack(pady=10)
        tk.Button(janela, text="Fechar programa", width=40, height=2,
                  command=lambda: (janela.destroy(), self.fechar_programa())
                 ).pack(pady=10)
        self.centralizar_janela(janela)
        janela.mainloop()

    # --- Função que cria o banco, insere o admin se necessário e chama a tela de login ---
    def criar_banco(self):
        # Conecta ao banco, utilizando os métodos do Model
        self.model.conexao = sqlite3.connect('users.db')
        self.model.cursor = self.model.conexao.cursor()
        self.model.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL DEFAULT 'senha123',
                tipo TEXT NOT NULL DEFAULT 'usuario'
            )
        ''')
        # Verifica se o usuário admin já existe. Se não, insere-o.
        self.model.cursor.execute("SELECT * FROM usuarios WHERE nome = ? OR email = ?", ("admin", "adminn@gmail.com"))
        existe = self.model.cursor.fetchone()
        if not existe:
            self.model.cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, tipo)
                VALUES (?, ?, ?, ?)
            ''', ("admin", "adminn@gmail.com", "admin123", "admin"))
            print("Usuário administrador criado com sucesso!")
        else:
            print("Usuário admin já existe.")
        # Exibe todos os usuários do banco no console

        self.model.conexao.commit()
        self.model.conexao.close()
        
        # Após criar o banco, chama a tela de login
        self.tela_login()

    # --- Tela do usuário (apresenta painel de usuário) ---
    def tela_usuario(self, nome, senha):
        janela = tk.Tk()
        janela.title("Painel de Usuário")
        self.centralizar_janela(janela, 600, 450)
        # Busca o email do usuário no banco
        self.model.cursor.execute("SELECT email FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        resultado = self.model.cursor.fetchone()
        email = resultado[0] if resultado else "Email não encontrado"
        tk.Label(janela, text=f"Bem-vindo, {nome}!", font=("Arial", 14)).pack(pady=10)
        # Cria uma listbox para mostrar os dados do usuário
        listbox = tk.Listbox(janela, width=80, height=10)
        listbox.pack()

        def carregar_usuarios():
            # Limpa a listbox antes de carregar os dados
            listbox.delete(0, tk.END)
            self.model.cursor.execute("SELECT nome, email, senha from usuarios WHERE nome = ? AND senha = ?", (nome, senha))\
            # Insere os dados do usuário na listbox
            for usuario in self.model.cursor.fetchall():
                listbox.insert(tk.END, f"nome: {usuario[0]}")
                listbox.insert(tk.END, f"email: {usuario[1]}")
                listbox.insert(tk.END, f"senha: {usuario[2]}")
            listbox.insert(tk.END, "-" * 40)
            
        carregar_usuarios()

        def alterar_senha():
            # Altera a senha do usuário
            selecionado = listbox.curselection()
            if selecionado:
                dados = listbox.get(selecionado).split(" | ")
                id_usuario = dados[0]
                nova_senha = simpledialog.askstring("Alterar Senha", "Digite a nova senha:", show="*")
                # Verifica se a nova senha possui pelo menos 6 caracteres
                if nova_senha and len(nova_senha) >= 6:
                    self.model.cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (nova_senha, id_usuario))
                    self.model.conexao.commit()
                    messagebox.showinfo("Sucesso", "Senha atualizada.")
                else:
                    messagebox.showwarning("Erro", "Senha inválida. Mínimo 6 caracteres.")
            else:
                messagebox.showwarning("Atenção", "Selecione um usuário para alterar a senha.")

        def alterar_email():\
            # Altera o email do usuário
            selecionado = listbox.curselection()
            if selecionado:
                dados = listbox.get(selecionado).split(" | ")
                id_usuario = dados[0]
                novo_email = simpledialog.askstring("Alterar Email", "Digite o novo email:")
                # Verifica se o email possui um '@' e um ponto
                if novo_email.count('@') == 1 and '.' in novo_email:
                    self.model.cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (novo_email, id_usuario))
                    self.model.conexao.commit()
                    messagebox.showinfo("Sucesso", "Email atualizado.")
                else:
                    messagebox.showwarning("Erro", "Email inválido.")
            else:
                messagebox.showwarning("Atenção", "Selecione um usuário para alterar o email.")

        tk.Button(janela, text="Alterar senha", width=40, height=3, command=alterar_senha).pack(pady=10)
        tk.Button(janela, text="Alterar email", width=40, height=3, command=alterar_email).pack(pady=10)
        
        # Cria um frame para os botões inferiores
        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(pady=10)
        
        # Botões de logout e fechar programa
        tk.Button(frame_botoes, text="Logout", width=20, height=3,
                  command=lambda: (janela.destroy(), self.tela_login())
                 ).pack(side="left", padx=5)
        
        tk.Button(frame_botoes, text="Fechar programa", width=20, height=3,
                  command=lambda: (janela.destroy(), self.fechar_programa())
                 ).pack(side="left", padx=5)
        janela.mainloop()

    def tela_admin(self):
        # Cria a janela de administração
        
        janela = tk.Tk()
        janela.title("Painel de Administração")
        self.centralizar_janela(janela, 600, 450)
        tk.Label(janela, text="Usuários cadastrados:").pack(pady=10)

        def buscar_usuario():
            # Busca usuários pelo nome digitado na entry_busca
            termo = entry_busca.get()
            listbox.delete(0, tk.END)
            self.model.cursor.execute("SELECT id, nome, email, tipo FROM usuarios WHERE nome LIKE ?", (f"%{termo}%",))
            for usuario in self.model.cursor.fetchall():
                listbox.insert(tk.END, f"{usuario[0]} | {usuario[1]} | {usuario[2]} | {usuario[3]}")

        def carregar_usuarios():
            # Carrega todos os usuários do banco e os exibe na listbox
            listbox.delete(0, tk.END)
            self.model.cursor.execute("SELECT id, nome, email, tipo FROM usuarios")
            for usuario in self.model.cursor.fetchall():
                listbox.insert(tk.END, f"{usuario[0]} | {usuario[1]} | {usuario[2]} | {usuario[3]}")

        # Cria o frame e os widgets de busca sem alteração
        frame_busca = tk.Frame(janela)
        frame_busca.pack(pady=5)
        tk.Label(frame_busca, text="Buscar por nome:").pack(side="left")
        # Entry para busca de usuários
        entry_busca = tk.Entry(frame_busca, width=30)
        entry_busca.pack(side="left", padx=5)
        # Botões de busca e mostrar todos
        tk.Button(frame_busca, text="Buscar", command=buscar_usuario).pack(side="left", padx=5)
        tk.Button(frame_busca, text="Mostrar Todos", command=carregar_usuarios).pack(side="left")
        # Cria a listbox para exibir os usuários
        listbox = tk.Listbox(janela, width=80, height=10)
        listbox.pack()
        carregar_usuarios()

        def exportar_csv():
            # Exporta os usuários para um arquivo CSV
            self.model.cursor.execute("SELECT id, nome, email, tipo FROM usuarios")
            usuarios = self.model.cursor.fetchall()
            with open("usuarios_exportados.csv", "w", newline="", encoding="utf-8") as arquivo:
                writer = csv.writer(arquivo, delimiter=';')  # <- apenas esse
                writer.writerow(["ID", "Nome", "Email", "Tipo"])
                writer.writerows(usuarios)
            messagebox.showinfo("Exportação", "Usuários exportados com sucesso!")
        tk.Button(janela, text="Exportar para CSV", width=30, command=exportar_csv).pack(pady=5)

        def deletar_usuario():
            # Deleta o usuário selecionado na listbox
            selecionado = listbox.curselection()
            if selecionado:
                dados = listbox.get(selecionado).split(" | ")
                id_usuario = dados[0]
                self.model.cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
                self.model.conexao.commit()
                carregar_usuarios()
                messagebox.showinfo("Sucesso", "Usuário deletado.")
            else:
                messagebox.showwarning("Atenção", "Selecione um usuário para deletar.")

        def alterar_senha():
            # Altera a senha do usuário selecionado na listbox
            selecionado = listbox.curselection()
            if selecionado:
                dados = listbox.get(selecionado).split(" | ")
                id_usuario = dados[0]
                nova_senha = simpledialog.askstring("Alterar Senha", "Digite a nova senha:", show="*")
                if nova_senha and len(nova_senha) >= 6:
                    self.model.cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (nova_senha, id_usuario))
                    self.model.conexao.commit()
                    messagebox.showinfo("Sucesso", "Senha atualizada.")
                else:
                    messagebox.showwarning("Erro", "Senha inválida. Mínimo 6 caracteres.")
            else:
                messagebox.showwarning("Atenção", "Selecione um usuário para alterar a senha.")
                
        ## Cria os botões de administração
        tk.Button(janela, text="Deletar Usuário", width=40, height=2,
                  command=deletar_usuario).pack(pady=5)
        
        tk.Button(janela, text="Alterar Senha", width=40, height=2,
                  command=alterar_senha).pack(pady=5)
        
        tk.Button(janela, text="Cadastrar Novo Usuário Admin", width=40, height=2,
                  command=lambda: (janela.destroy(), self.cadastrar_usuario(tipo='admin'))).pack(pady=10)
        
        # Cria um frame para os botões inferiores
        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(pady=10)
        
        # Botões de logout e fechar programa
        tk.Button(frame_botoes, text="Logout", width=20, height=2,
                  command=lambda: (janela.destroy(), self.tela_login())).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar programa", width=20, height=2,
                  command=lambda: (janela.destroy(), self.fechar_programa())).pack(side="left", padx=5)
        
        # Centraliza a janela e inicia o loop principal
        self.centralizar_janela(janela, 600, 550)
        janela.update_idletasks()  # Atualiza o layout da janela
        janela.mainloop()

    # --- Função de login ---
    def login(self, entry_nome, entry_senha, janela):
        nome = entry_nome.get()
        senha = entry_senha.get()
        if nome and senha:
            # Verifica as credenciais no banco
            self.model.cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
            usuario = self.model.cursor.fetchone()
            if usuario:
                janela.withdraw()  # Esconde a janela de login
                # Recupera o tipo do usuário (admin ou usuário comum)
                self.model.cursor.execute("SELECT tipo FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
                tipo_usuario = self.model.cursor.fetchone()
                if tipo_usuario[0] == "admin": # Se for admin, chama a tela de administração
                    self.tela_admin()
                else:
                    # Se for usuário comum, chama a tela de usuário
                    self.tela_usuario(nome, senha)
                entry_nome.delete(0, tk.END)
                entry_senha.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")


# CONTROLLER: integra Model e View)
class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()
        self.view = UsuarioView(self.model)

    def iniciar(self):
        # Cria o banco e inicia a aplicação na tela de login
        self.view.criar_banco()

if __name__ == "__main__":
    app = UsuarioController()
    app.iniciar()