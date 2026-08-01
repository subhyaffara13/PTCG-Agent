
def get_data() -> dict[str, Any]:
    """
    returns a dict of various user environment data
    """
    env: dict[str, Any] = {}
    env["path"] = os.environ.get("PATH")
    env["sys_path"] = sys.path
    env["sys_exe"] = sys.executable
    env["sys_version"] = sys.version
    env["platform"] = platform.platform()
    # FIXME: which on Windows?
    if sys.platform == "win32":
        env["where"] = subs(["where", "jupyter"])
        env["which"] = None
    else:
        env["which"] = subs(["which", "-a", "jupyter"])
        env["where"] = None
    env["pip"] = subs([sys.executable, "-m", "pip", "list"])
    env["conda"] = subs(["conda", "list"])
    env["conda-env"] = subs(["conda", "env", "export"])
    return env

