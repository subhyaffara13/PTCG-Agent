
def getsearchdirs() -> tuple[list[str], list[str]]:
    return (getsyspath(), getsitepackages())

