import tkinter as tk
from tkinter import messagebox
import subprocess

# Função para executar comandos Git e obter saída
def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.returncode

# Função para criar o commit com a mensagem
def git_commit(commit_type, example_message):
    def commit():
        commit_message = commit_text.get("1.0", tk.END).strip()
        if commit_message:
            output, code = run_git_command(f'git commit -m "{commit_message}"')
            if code == 0:
                confirmation_message = f"Commit realizado com sucesso!\n\n{output}"
                messagebox.showinfo("Git Commit", confirmation_message)
                console_output.insert(tk.END, confirmation_message, "yellow")
            else:
                error_message = f"Falha ao realizar commit.\n\n{output}"
                messagebox.showerror("Erro", error_message)
                console_output.insert(tk.END, error_message, "yellow")
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
    output, code = run_git_command("git push")
    if code == 0:
        confirmation_message = f"Push realizado com sucesso!\n\n{output}"
        messagebox.showinfo("Git Push", confirmation_message)
        console_output.insert(tk.END, confirmation_message, "yellow")
    else:
        error_message = f"Falha ao realizar push.\n\n{output}"
        messagebox.showerror("Erro", error_message)
        console_output.insert(tk.END, error_message, "yellow")

# Função para aplicar cores ao texto do status do Git
def colorize_git_status(status_output):
    console_output.tag_configure("green", foreground="green")
    console_output.tag_configure("red", foreground="red")
    console_output.tag_configure("yellow", foreground="yellow")
    console_output.tag_configure("white", foreground="white")

    lines = status_output.split('\n')
    for line in lines:
        if line.startswith('\tnew file:'):
            console_output.insert(tk.END, line + '\n', "green")
        elif line.startswith('\tmodified:'):
            console_output.insert(tk.END, line + '\n', "red")
        else:
            console_output.insert(tk.END, line + '\n', "white")

# Função para exibir a saída do comando git push no campo de texto
def display_git_push_output():
    output, code = run_git_command("git push")
    if code == 0:
        confirmation_message = f"Push realizado com sucesso!\n\n{output}"
        console_output.insert(tk.END, confirmation_message, "yellow")
    else:
        error_message = f"Falha ao realizar push.\n\n{output}"
        console_output.insert(tk.END, error_message, "yellow")

# Criação da interface gráfica principal
root = tk.Tk()
root.title("Git GUI")

console_output = tk.Text(root, height=10, width=100, bg="black", fg="white")
console_output.pack()

tk.Label(root, text="Tipos de Commit:").pack()

commit_types = {
    "fix": "fix(webview): Fixed video display in WebView on Android: the control was forced to use software rendering.",
    "feat": "feat(imageBrush): [iOS][macOS] Add support of WriteableBitmap",
    "docs": "docs: atualiza README com instruções de setup",
    "style": "style: formata código conforme padrão de estilo",
    "refactor": "refactor: refatora o módulo de autenticação",
    "test": "test: adiciona testes unitários para o módulo de pagamentos",
    "chore": "chore: Fix XAML parsing sample",
    "fix_breaking": "fix(resourcedictionary)!: Make ResourceDictionary.Lookup() internal, use correct lookup\n\nBREAKING CHANGE: This method isn't part of the public .NET contract on WinUI. Use item indexing or TryGetValue() instead."
}

button_frame = tk.Frame(root)
button_frame.pack()

for ctype, example in commit_types.items():
    tk.Button(button_frame, text=ctype, command=lambda c=ctype, e=example: git_commit(c, e)).pack(side="left")

tk.Button(root, text="Realizar Push", command=display_git_push_output).pack()

# Iniciando o script
print("Executando git status...")
status_output, status_code = run_git_command("git status")
print(status_output)

if status_code == 0:
    colorize_git_status(status_output)
else:
    error_message = f"Falha ao obter status do Git.\n\n{status_output}"
    messagebox.showerror("Erro", error_message)
    console_output.insert(tk.END, error_message, "yellow")

root.mainloop()

