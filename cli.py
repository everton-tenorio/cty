import argparse
import subprocess
import os


def run_git_command(command_list):
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True)
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        # Retorna a saída e o código de erro em caso de falha
        return e.output, e.returncode
    except FileNotFoundError as e:
        # Trata o caso em que o comando não foi encontrado
        return str(e), 1


def print_boxed_message(title, message):
    border_char = "="
    message_lines = message.splitlines()
    max_line_length = max(len(line) for line in message_lines)
    border_length = max_line_length + 4

    # Print top border
    print(f"{border_char * border_length}")

    # Print title
    title_line = f"{title.center(max_line_length)}"
    print(f"{border_char} {title.center(max_line_length)} {border_char}")

    # Print message with borders
    for line in message_lines:
        print(f"{border_char} {line.ljust(max_line_length)} {border_char}")

    # Print bottom border
    print(f"{border_char * border_length}")


# Função para gerar mensagem de commit de exemplo com base no tipo
def get_commit_message(commit_type, use_emoji):
    messages = {
        "fix": "fix: corrigido erro no sistema",
        "feat": "feat: adicionada nova funcionalidade",
        "docs": "docs: atualizado README",
        "style": "style: ajustado estilo do código",
        "refactor": "refactor: refatorado código para melhorar desempenho",
        "test": "test: adicionados novos testes",
        "chore": "chore: realizado manutenção geral",
        "build": "build: Alterações que afetam o sistema de build ou dependências externas | atualizado pacote de dependências",
        "ci": "ci: Configurações de integração contínua | ajustada configuração do pipeline de CI",
        "perf": "perf: Melhorias no desempenho | ex.: otimizado carregamento de página",
        "revert": "revert: Reversão de um commit anterior | revertido commit 123abc",
    }
    
    emoji_messages = {
        "fix": "🪲 fix: corrigido erro no sistema",
        "feat": "🚀 feat: adicionada nova funcionalidade",
        "docs": "📚 docs: atualizado README",
        "style": "🎨 style: ajustado estilo do código",
        "refactor": "🔨 refactor: refatorado código para melhorar desempenho",
        "test": "🧪 test: adicionados novos testes",
        "chore": "🧹 chore: realizado manutenção geral",
        "build": "📦 build: Alterações que afetam o sistema de build ou dependências externas | atualizado pacote de dependências",
        "ci": "🤖 ci: Configurações de integração contínua | ajustada configuração do pipeline de CI",
        "perf": "🚀 perf: Melhorias no desempenho | ex.: otimizado carregamento de página",
        "revert": "↩️  revert: Reversão de um commit anterior | revertido commit 123abc",
    }
    
    if use_emoji:
        return emoji_messages.get(commit_type, "Tipo de commit desconhecido")
    else:
        return messages.get(commit_type, "Tipo de commit desconhecido")


def main():
    parser = argparse.ArgumentParser(description="CONVC = Conventional Commits CLI \n  # use: convc <option> <type>")
    parser.add_argument('-t', '--type', required=True, choices=['fix', 'feat', 'docs', 'style', 'refactor', 'test', 'chore', 'build', 'ci', 'perf', 'revert'],
                        help='Tipo de commit (fix, feat, docs, style, refactor, test, chore, build, ci, perf, revert)')
    parser.add_argument('--emoji', '-e', action='store_true', help="Tipo com emojis no commit")

    args = parser.parse_args()

    # Gerar mensagem de exemplo
    commit_type = args.type
    use_emoji = args.emoji

    # Obter a mensagem de commit
    commit_message = get_commit_message(commit_type, use_emoji)

    # Criar o arquivo temporário com a mensagem exemplo
    temp_file = "commit_message.txt"
    with open(temp_file, "w") as f:
        f.write(f"{commit_message}\n\n")

    # Abrir o Vim com o arquivo temporário
    print(f"\n📜 A mensagem de commit foi salva em '{temp_file}'. Editando no Vim...\n")
    vim_path = "/usr/bin/vim"
    subprocess.run([vim_path, temp_file], check=True)

    # Realizar o commit usando o arquivo de mensagem
    print(f"🔄 Realizando commit com a mensagem em '{temp_file}'...\n")
    commit_output, commit_code = run_git_command(["git", "commit", "-F", temp_file])

    if commit_code == 0:
        # Captura o hash e a mensagem do commit mais recente
        log_output, log_code = run_git_command(["git", "log", "-1", "--format=%H %s"])
        if log_code == 0:
            commit_hash, commit_message = log_output.strip().split(' ', 1)

            success_message = f"Commit realizado com sucesso!\n\nCommit: {commit_hash} \nMensagem: {commit_message}\n"
            print_boxed_message("✅ Commit Realizado!", success_message)

        else:
            print(f"\n❌ Falha ao obter o log do commit:\n{log_output.strip()}")
    else:
        print(f"\n❌ Falha ao realizar commit:\n{commit_output.strip()}")  # Exibir a saída de erro detalhada


    # Remover o arquivo temporário
    os.remove(temp_file)
    print(f"\n🗑️ Arquivo temporário '{temp_file}' excluído.\n Problemas com o último commit? Reset com: git reset --soft HEAD~1")

if __name__ == "__main__":
    main()

