
def invoke_install(path, *, dependency_group=None, **kwargs):
    try:
        call(
            "install", "--requirement", dependency_group or "requirements.txt", cwd=path
        )
    except subprocess.CalledProcessError as e:
        return e.returncode
    return 0

