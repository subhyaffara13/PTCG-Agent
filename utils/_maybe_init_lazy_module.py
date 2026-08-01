
def _maybe_init_lazy_module(obj: object) -> None:
    module = getattr(obj, "__module__", None)
    if module is None:
        return

    base_module = module.split(".")[0]
    init_funcs = _lazy_module_init.pop(base_module, None)
    if init_funcs is not None:
        for fn in init_funcs:
            fn()

