
def export_case(**kwargs):
    """
    Decorator for registering a user provided case into example bank.
    """

    def wrapper(m):
        configs = kwargs
        module = inspect.getmodule(m)
        if module in _MODULES:
            raise RuntimeError("export_case should only be used once per example file.")

        if module is None:
            raise AssertionError("module must not be None")
        _MODULES.add(module)
        module_name = module.__name__.split(".")[-1]
        case = _make_export_case(m, module_name, configs)
        register_db_case(case)
        return case

    return wrapper

