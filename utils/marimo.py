import subprocess

def marimo(*args: str):
    cmd = ["marimo"] + list(args)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise MarimoError(f"marimo exited with return code {proc.returncode}\n{str(err)}")

    return out.decode("utf-8")

