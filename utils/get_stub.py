
def get_stub(module: str) -> nodes.MypyFile | None:
    """Returns a stub object for the given module, if we've built one."""
    return _all_stubs.get(module)

