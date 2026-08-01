
def make_module(mod, _module_class, _compilation_unit):
    if isinstance(mod, ScriptModule):
        return mod
    elif torch._jit_internal.module_has_exports(mod):
        infer_methods_stubs_fn = torch.jit._recursive.make_stubs_from_exported_methods
        return torch.jit._recursive.create_script_module(
            mod, infer_methods_stubs_fn, share_types=False, is_tracing=True
        )
    else:
        if _module_class is None:
            _module_class = TopLevelTracedModule
        return _module_class(mod, _compilation_unit=_compilation_unit)

