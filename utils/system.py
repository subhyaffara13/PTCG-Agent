
def system(*args, **kwargs):
    """Execute the given bash command"""
    kwargs.setdefault("stdout", subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _ = proc.communicate()
    if proc.returncode:
        raise SystemExit(proc.returncode)
    return out.decode("utf-8")

