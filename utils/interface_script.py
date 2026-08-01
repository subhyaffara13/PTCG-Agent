
def interface_script(mod_interface, nn_module):
    """
    Make a ScriptModule from an nn.Module, using the interface methods rule for determining which methods to compile.

    Args:
        mod_interface: the interface type that the module have
        nn_module:  The original Python nn.Module that we are creating a ScriptModule for.
    """
    if isinstance(nn_module, torch.jit.ScriptModule):
        return nn_module

    check_module_initialized(nn_module)

    def infer_interface_methods_to_compile(nn_module):
        """Rule to infer the methods from the interface type.

        It is used to know which methods need to act as starting points for compilation.
        """
        stubs = [
            make_stub_from_method(nn_module, method)
            for method in mod_interface.getMethodNames()
        ]
        return stubs

    return create_script_module(nn_module, infer_interface_methods_to_compile)

