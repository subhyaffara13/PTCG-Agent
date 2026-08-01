
def _get_login_shell(proc_cmd):
    """Form shell information from SHELL environ if possible."""
    login_shell = os.environ.get("SHELL", "")
    if login_shell:
        proc_cmd = login_shell
    else:
        proc_cmd = proc_cmd[1:]
    return (os.path.basename(proc_cmd).lower(), proc_cmd)

