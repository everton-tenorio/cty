import argparse
import subprocess
import os


def run_git_command(command_list):
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True)
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        # Returns the output and error code in case of failure
        return e.output, e.returncode
    except FileNotFoundError as e:
        # Handles the case where the command was not found
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


# Function to generate example commit message based on type
def get_commit_message(commit_type, use_emoji):
    messages = {
        "fix": "fix: system error fixed",
        "feat": "feat: new feature added",
        "docs": "docs: README updated",
        "style": "style: code style adjusted",
        "refactor": "refactor: code refactored for better performance",
        "test": "test: new tests added",
        "chore": "chore: general maintenance done",
        "build": "build: Changes affecting the build system or external dependencies | updated dependencies package",
        "ci": "ci: Continuous integration settings | CI pipeline configuration adjusted",
        "perf": "perf: Performance improvements | e.g., optimized page load",
        "revert": "revert: Reverted a previous commit | reverted commit 123abc",
    }
    
    emoji_messages = {
        "fix": "🪲 fix: system error fixed",
        "feat": "🚀 feat: new feature added",
        "docs": "📚 docs: README updated",
        "style": "🎨 style: code style adjusted",
        "refactor": "🔨 refactor: code refactored for better performance",
        "test": "🧪 test: new tests added",
        "chore": "🧹 chore: general maintenance done",
        "build": "📦 build: Changes affecting the build system or external dependencies | updated dependencies package",
        "ci": "🤖 ci: Continuous integration settings | CI pipeline configuration adjusted",
        "perf": "🚀 perf: Performance improvements | e.g., optimized page load",
        "revert": "↩️  revert: Reverted a previous commit | reverted commit 123abc",
    }
    
    if use_emoji:
        return emoji_messages.get(commit_type, "Unknown commit type")
    else:
        return messages.get(commit_type, "Unknown commit type")


def main():
    parser = argparse.ArgumentParser(description="cty - Conventional Commits CLI")
    parser.add_argument('-t', '--type', required=True, choices=['fix', 'feat', 'docs', 'style', 'refactor', 'test', 'chore', 'build', 'ci', 'perf', 'revert'],
                        help='Commit type (fix, feat, docs, style, refactor, test, chore, build, ci, perf, revert)')
    parser.add_argument('--emoji', '-e', action='store_true', help="Commit type with emojis")

    args = parser.parse_args()

    # Generate example message
    commit_type = args.type
    use_emoji = args.emoji

    # Get the commit message
    commit_message = get_commit_message(commit_type, use_emoji)

    # Create the temporary file with the example message
    temp_file = "commit_message.txt"
    with open(temp_file, "w") as f:
        f.write(f"{commit_message}\n\n")

    # Open Vim with the temporary file
    print(f"\n📜 The commit message has been saved in '{temp_file}'. Editing in Vim...\n")
    vim_path = "/usr/bin/vim"
    subprocess.run([vim_path, temp_file], check=True)

    # Perform the commit using the message file
    print(f"🔄 Performing commit with the message in '{temp_file}'...\n")
    commit_output, commit_code = run_git_command(["git", "commit", "-F", temp_file])

    if commit_code == 0:
        # Capture the hash and message of the most recent commit
        log_output, log_code = run_git_command(["git", "log", "-1", "--format=%H %s"])
        if log_code == 0:
            commit_hash, commit_message = log_output.strip().split(' ', 1)

            success_message = f"Commit successfully made!\n\nCommit: {commit_hash} \nMessage: {commit_message}\n"
            print_boxed_message("✅ Commit Made!", success_message)

        else:
            print(f"\n❌ Failed to get commit log:\n{log_output.strip()}")
    else:
        print(f"\n❌ Failed to commit:\n{commit_output.strip()}")  # Display detailed error output


    # Remove the temporary file
    os.remove(temp_file)
    print(f"\n🗑️ Temporary file '{temp_file}' deleted.\n Problems with the last commit? Reset with: git reset --soft HEAD~1")

if __name__ == "__main__":
    main()
