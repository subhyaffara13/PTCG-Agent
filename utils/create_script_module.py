
def create_script_module(nn_module, stubs_fn, share_types=True, is_tracing=False):
    """
    Create a new ScriptModule from an nn.Module.

    Args:
        nn_module:  The original Python nn.Module that we are creating a ScriptModule for.
        stubs_fn:  Lambda that takes an nn.Module and generates a list of ScriptMethodStubs to compile.
        share_types:  Whether to share underlying JIT types between modules (if possible).
            NOTE: Only set to False this when we cannot guarantee type sharing will work
                correctly. This only happens today for traced modules, where the same
                module can produce different traced methods depending on the inputs.
        is_tracing: Whether this function is called during tracing or scripting. If tracing,
                we don't need to do AttributeTypeIsSupportedChecker because all the unsupported
                attributes will be baked as constant in the tracing graph. In addition,
                this check significantly slows down the traced modules when the module size is big.
    """
    if isinstance(nn_module, torch.jit.RecursiveScriptModule):
        raise AssertionError("Cannot script a RecursiveScriptModule (already compiled)")
    check_module_initialized(nn_module)
    concrete_type = get_module_concrete_type(nn_module, share_types)
    if not is_tracing:
        AttributeTypeIsSupportedChecker().check(nn_module)
    return create_script_module_impl(nn_module, concrete_type, stubs_fn)


def create_script_module(self, nn_module, constructor_args, *args, **kwargs):
    def script_module(*args, **kwargs):
        _formals, tensors, actuals = get_script_args(args)

        method_args = ', '.join(['self'] + actuals)
        call_args_str = ', '.join(actuals)
        call = f"self.submodule({call_args_str})"
        script = script_method_template.format(method_args, call)

        submodule_constants = []
        if kwargs.get('is_constant'):
            submodule_constants = ['submodule']

        # Create module to use the script method
        class TheModule(torch.jit.ScriptModule):
            __constants__ = submodule_constants

            def __init__(self) -> None:
                super().__init__()
                self.submodule = nn_module(*constructor_args)

        def make_module(script):
            module = TheModule()
            # check __repr__
            str(module)
            module.define(script)
            return module

        module = make_module(script)
        if self:
            self.assertExportImportModule(module, tensors)
            module(*args)
        # skip type annotate function attributes for now, see: https://github.com/python/mypy/issues/2087
        create_script_module.last_graph = module.graph  # type: ignore[attr-defined]
        return module
    return script_module

