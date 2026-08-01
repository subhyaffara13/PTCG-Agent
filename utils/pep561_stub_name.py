
def pep561_stub_name(value: str) -> bool:
    """Name of a directory containing type stubs.
    It must follow the name scheme ``<package>-stubs`` as defined in
    :pep:`561#stub-only-packages`.
    """
    top, *children = value.split(".")
    if not top.endswith("-stubs"):
        return False
    return python_module_name(".".join([top[: -len("-stubs")], *children]))

