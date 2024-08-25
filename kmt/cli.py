import argparse
import subprocess
import os

# Função para executar comandos Git e obter saída
def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.returncode


def print_boxed_message(title, message):
    border_char = "="
    message_lines = message.splitlines()
    max_line_length = max(len(line) for line in message_lines)
    border_length = max_line_length + 4

    # Print top border
    print(f"{border_char * border_length}")

    # Print title
    print(f"{border_char} {title.center(max_line_length)} {border_char}")

    # Print message with borders
    for line in message_lines:
        print(f"{border_char} {line.ljust(max_line_length)} {border_char}")

    # Print bottom border
    print(f"{border_char * border_length}")


# Função para gerar mensagem de commit de exemplo com base no tipo
def get_commit_example(commit_type):
    commit_types = {
        "fix": "fix(webview): Fixed video display in WebView on Android: the control was forced to use software rendering.",
        "feat": "feat(imageBrush): [iOS][macOS] Add support of WriteableBitmap",
        "docs": "docs: atualiza README com instruções de setup",
        "style": "style: formata código conforme padrão de estilo",
        "refactor": "refactor: refatora o módulo de autenticação",
        "test": "test: adiciona testes unitários para o módulo de pagamentos",
        "chore": "chore: Fix XAML parsing sample",
        "fix_breaking": "fix(resourcedictionary)!: Make ResourceDictionary.Lookup() internal, use correct lookup\n\nBREAKING CHANGE: This method isn't part of the public .NET contract on WinUI. Use item indexing ou TryGetValue() instead."
    }
    return commit_types.get(commit_type, "Tipo de commit não reconhecido.")

def main():
    parser = argparse.ArgumentParser(description="Ferramenta de Conventional Commits CLI")
    parser.add_argument('-t', '--type', required=True, choices=['fix', 'feat', 'docs', 'style', 'refactor', 'test', 'chore', 'fix_breaking'],
                        help='Tipo de commit (fix, feat, docs, style, refactor, test, chore, fix_breaking)')
    
    args = parser.parse_args()
    
    # Gerar mensagem de exemplo
    example_message = get_commit_example(args.type)
    
    # Criar o arquivo temporário com a mensagem exemplo
    temp_file = "commit_message.txt"
    with open(temp_file, "w") as f:
        f.write(f"{example_message}\n\n")
    
    # Abrir o Vim com o arquivo temporário
    print(f"\n📜 A mensagem de commit foi salva em '{temp_file}'. Editando no Vim...\n")
    subprocess.run(["vim", temp_file])

    # Realizar o commit usando o arquivo de mensagem
    print(f"\n🔄 Realizando commit com a mensagem em '{temp_file}'...\n")
    commit_output, commit_code = run_git_command(f"git commit -F {temp_file}")

    if commit_code == 0:
        # Captura o hash e a mensagem do commit mais recente
        log_output, log_code = run_git_command(f'git log -1 "--format=%H %s"')
        if log_code == 0:
            commit_hash, commit_message = log_output.strip().split(' ', 1)

            #print(f"\n✅ Commit realizado com sucesso!\n")
            #print(f"Commit: {commit_hash}\nMensagem: {commit_message}\n")
            success_message = f"Commit realizado com sucesso!\n\nCommit: {commit_hash}\nMensagem: {commit_message}\n"
            print_boxed_message("✅ Commit Realizado Com Sucesso", success_message)

        else:
            print(f"\n❌ Falha ao obter o log do commit:\n{log_output.strip()}")
    else:
        print(f"\n❌ Falha ao realizar commit:\n{commit_output.strip()}")  # Exibir a saída de erro detalhada


    # Remover o arquivo temporário
    os.remove(temp_file)
    print(f"\n🗑️ Arquivo temporário '{temp_file}' excluído.")

if __name__ == "__main__":
    main()

