from pathlib import Path


def install_zsh(*, prog_name: str, complete_var: str, shell: str) -> Path:
    # Setup Zsh and load ~/.zfunc
    zshrc_path = Path.home() / ".zshrc"
    zshrc_path.parent.mkdir(parents=True, exist_ok=True)
    zshrc_content = ""
    if zshrc_path.is_file():
        zshrc_content = zshrc_path.read_text()
    completion_line = "fpath+=~/.zfunc; autoload -Uz compinit; compinit"
    if completion_line not in zshrc_content:
        zshrc_content += f"\n{completion_line}\n"
    style_line = "zstyle ':completion:*' menu select"
    # TODO: consider setting the style only for the current program
    # style_line = f"zstyle ':completion:*:*:{prog_name}:*' menu select"
    # Install zstyle completion config only if the user doesn't have a customization
    if "zstyle" not in zshrc_content:
        zshrc_content += f"\n{style_line}\n"
    zshrc_content = f"{zshrc_content.strip()}\n"
    zshrc_path.write_text(zshrc_content)
    # Install completion under ~/.zfunc/
    path_obj = Path.home() / f".zfunc/_{prog_name}"
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    path_obj.write_text(script_content)
    return path_obj

