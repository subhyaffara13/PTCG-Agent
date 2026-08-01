
def add_module_init_func(name: str, init_func: Callable[[], None]) -> None:
    """Register a module without eagerly importing it"""
    # If the module is already imported, eagerly run init
    assert "." not in name, f"Expected a root module name, but got {name}"
    assert name not in _lazy_module_init
    _lazy_module_init[name].append(init_func)

