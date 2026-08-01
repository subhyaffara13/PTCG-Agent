
def _exec(obj):
    # exec on PyQt6, exec_ elsewhere.
    obj.exec() if hasattr(obj, "exec") else obj.exec_()


def _exec(path: str, args: Sequence[str], env: Mapping[str, str]) -> None:
    os.execvpe(path, list(args), dict(env))

