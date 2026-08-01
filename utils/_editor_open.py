
def _editor_open(local_path: str) -> int | Literal["no-tty", "no-editor"]:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return "no-tty"
    if (editor_command := _get_editor_command()) is None:
        return "no-editor"
    command = [*shlex.split(editor_command), local_path]
    res = subprocess.run(command, start_new_session=True)
    return res.returncode

