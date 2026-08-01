
def dispatch_unknown_top_level_extension(args: list[str], known_commands: set[str]) -> int | None:
    if not args:
        return None

    command_name = args[0]
    if command_name.startswith("-"):
        return None
    all_known = {a.strip() for cmd in known_commands for a in cmd.split("|")}
    if command_name in all_known:
        return None

    short_name = command_name[3:] if command_name.startswith("hf-") else command_name
    if not short_name:
        return None

    executable_path: Path | None = None
    try:
        executable_path = _resolve_installed_executable_path(short_name)
    except Exception:
        executable_path = _auto_install_official_extension(short_name)

    if executable_path is None or not executable_path.is_file():
        return None

    return _execute_extension_binary(executable_path=executable_path, args=list(args[1:]))

