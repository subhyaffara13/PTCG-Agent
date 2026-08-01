
def iter_namespace_pkgs(namespace):
    parts = namespace.split(".")
    for i in range(len(parts)):
        yield ".".join(parts[: i + 1])

