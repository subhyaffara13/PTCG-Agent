import subprocess

def call_proc(cmd, cd=None):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cd,
        universal_newlines=True,
    )
    if proc.wait():
        print(f"{cmd} {proc.wait()}")
        raise Exception(proc.stdout.read())

    return proc.stdout.read()

