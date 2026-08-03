import subprocess

def vars():
    return lambda n: [var() for i in range(n)]


def vars():
    if not enabled():
        return {}
    homebrew_prefix = subprocess.check_output(['brew', '--prefix'], text=True).strip()
    return locals()

