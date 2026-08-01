
def guard_torch_init_functions():
    """
    Guard the `torch.nn.init` primitive functions to behave exactly like the functions in this file, i.e. be
    protected against the `_is_hf_initialized` flag to avoid re-init if the param was already loaded.

    Usually, all models are using the init from `transformers` which are already guarded, but just to make extra sure
    and for remote code, we also use this context manager.
    """
    originals = defaultdict(dict)
    try:
        # Replace all torch funcs by the ones in this file
        for module_name in TORCH_MODULES_TO_PATCH:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                for func_name in TORCH_INIT_FUNCTIONS.keys():
                    if hasattr(module, func_name):
                        originals[module][func_name] = getattr(module, func_name)
                        setattr(module, func_name, globals()[func_name])
        yield
    finally:
        # Set back the original functions on all modules
        for module, functions in originals.items():
            for func_name, func in functions.items():
                setattr(module, func_name, func)

