
def group_name(modules: list[str]) -> str:
    """Produce a probably unique name for a group from a list of module names."""
    if len(modules) == 1:
        return modules[0]

    h = hashlib.sha1()
    h.update(",".join(modules).encode())
    return h.hexdigest()[:20]

