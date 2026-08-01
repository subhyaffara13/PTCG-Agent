
def pandoc(args, filein=None, fileout=None):
    """Execute pandoc with the given arguments"""
    cmd = ["pandoc"]

    if filein:
        cmd.append(filein)

    if fileout:
        cmd.append("-o")
        cmd.append(fileout)

    cmd.extend(args.split())

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise PandocError(f"pandoc exited with return code {proc.returncode}\n{str(err)}")
    return out.decode("utf-8")

