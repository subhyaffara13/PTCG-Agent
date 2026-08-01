
def _get_shell(cmd, *args):
    if cmd.startswith("-"):  # Login shell! Let's use this.
        return _get_login_shell(cmd)
    name = os.path.basename(cmd).lower()
    if name == "rosetta" or QEMU_BIN_REGEX.fullmatch(name):
        # If the current process is Rosetta or QEMU, this likely is a
        # containerized process. Parse out the actual command instead.
        cmd = args[0]
        args = args[1:]
        name = os.path.basename(cmd).lower()
    if name in SHELL_NAMES:  # Command looks like a shell.
        return (name, cmd)
    shell = _get_interpreter_shell(name, args)
    if shell:
        return shell
    return None

