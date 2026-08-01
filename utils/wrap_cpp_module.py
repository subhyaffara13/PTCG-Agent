
def wrap_cpp_module(cpp_module):
    """Wrap this torch._C.ScriptModule in a Python ScriptModule, recursively for all submodules."""

    def init_fn(script_module) -> None:
        for name, cpp_module in torch._C.ModuleDict(script_module._c).items():
            setattr(script_module, name, wrap_cpp_module(cpp_module))
        script_module._concrete_type = torch._C.ConcreteModuleType.from_jit_type(
            script_module._c._type()
        )

        for idx, fn in enumerate(script_module._c._get_forward_pre_hooks()):
            script_module._forward_pre_hooks[idx] = fn
        for idx, fn in enumerate(script_module._c._get_forward_hooks()):
            script_module._forward_hooks[idx] = fn

    return torch.jit.RecursiveScriptModule._construct(cpp_module, init_fn)

