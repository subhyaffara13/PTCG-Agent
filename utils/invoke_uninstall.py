import subprocess

def invoke_uninstall(path, *, dependency_group=None, **kwargs):
    try:
        call(
            "uninstall",
            "--requirement",
            dependency_group or "requirements.txt",
            cwd=path,
        )
    except subprocess.CalledProcessError as e:
        return e.returncode
    return 0

