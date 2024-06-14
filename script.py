import tkinter as tk
from tkinter import messagebox
import subprocess

# Função para executar comandos Git e obter saída
def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

# Função para verificar o status do Git
def check_git_status():
    output = run_git_command("git status")
    status_text.insert(tk.END, output)

# Função para adicionar arquivos ao Git
def git_add():
    add_command = add_entry.get()
    run_git_command(add_command)
    messagebox.showinfo("Git Add", "Arquivos adicionados com sucesso!")

# Função para criar o commit com a mensagem
def git_commit(commit_type, example_message):
    def commit():
        commit_message = commit_text.get("1.0", tk.END).strip()
        if commit_message:
            run_git_command(f'git commit -m "{commit_message}"')
            messagebox.showinfo("Git Commit", "Commit realizado com sucesso!")
            commit_window.destroy()
        else:
            messagebox.showerror("Erro", "A mensagem do commit não pode estar vazia.")

    commit_window = tk.Toplevel(root)
    commit_window.title("Git Commit")

    tk.Label(commit_window, text="Mensagem do Commit:").pack()

    commit_text = tk.Text(commit_window, height=10, width=50)
    commit_text.pack()
    commit_text.insert(tk.END, f'{commit_type}: {example_message}\n')

    tk.Button(commit_window, text="Enviar", command=commit).pack()

# Função para realizar o push dos arquivos
def git_push():
    run_git_command("git push")
    messagebox.showinfo("Git Push", "Push realizado com sucesso!")

# Criação da interface gráfica principal
root = tk.Tk()
root.title("Git GUI")

tk.Label(root, text="Status do Git:").pack()

status_text = tk.Text(root, height=10, width=100)
status_text.pack()

tk.Button(root, text="Verificar Status", command=check_git_status).pack()

tk.Label(root, text="Adicionar Arquivos (e.g., 'git add .'):").pack()
add_entry = tk.Entry(root, width=100)
add_entry.pack()

tk.Button(root, text="Adicionar", command=git_add).pack()

tk.Label(root, text="Tipos de Commit:").pack()

commit_types = {
    "fix": "corrige um bug",
    "feat": "adiciona uma nova funcionalidade",
    "docs": "atualiza a documentação",
    "style": "formatação do código",
    "refactor": "refatoração do código",
    "test": "adiciona testes",
    "chore": "outras mudanças",
}

for ctype, example in commit_types.items():
    tk.Button(root, text=ctype, command=lambda c=ctype, e=example: git_commit(c, e)).pack()

tk.Button(root, text="Realizar Push", command=git_push).pack()

root.mainloop()
