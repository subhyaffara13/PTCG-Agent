
def create_signature_registry(module_info=module_info, signatures=signatures):
    for module, info in module_info.items():
        if isinstance(module, str):
            module = import_module(module)
        for name, sigs in info.items():
            if hasattr(module, name):
                new_sigs = tuple(expand_sig(sig) for sig in sigs)
                signatures[getattr(module, name)] = new_sigs

