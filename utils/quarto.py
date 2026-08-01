
def quarto(args, filein=None):
    """Execute quarto with the given arguments"""
    executable = shutil.which("quarto")
    if not executable and sys.platform.startswith("win"):
        # On Windows, try quarto.cmd, see #1406
        executable = shutil.which("quarto.cmd")
    if not executable:
        raise QuartoError("Could not find 'quarto' executable")

    cmd = [executable] + args.split()

    if filein:
        cmd.append(filein)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise QuartoError(f"{' '.join(cmd)} exited with return code {proc.returncode}\n{err.decode('utf-8')}")

    return out.decode("utf-8")

