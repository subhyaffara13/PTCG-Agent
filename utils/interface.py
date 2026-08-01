
def interface(obj: _T) -> _T:
    r"""Decorate to annotate classes or modules of different types.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.

    This decorator can be used to define an interface that can be used to annotate
    classes or modules of different types. This can be used for to annotate a submodule
    or attribute class that could have different types that implement the same
    interface, or which could be swapped at runtime; or to store a list of modules or
    classes of varying types.

    It is sometimes used to implement "Callables" - functions or modules that implement
    an interface but whose implementations differ and which can be swapped out.

    Example:
    .. testcode::

        import torch
        from typing import List

        @torch.jit.interface
        class InterfaceType:
            def run(self, x: torch.Tensor) -> torch.Tensor:
                pass

        # implements InterfaceType
        @torch.jit.script
        class Impl1:
            def run(self, x: torch.Tensor) -> torch.Tensor:
                return x.relu()

        class Impl2(torch.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.val = torch.rand(())

            @torch.jit.export
            def run(self, x: torch.Tensor) -> torch.Tensor:
                return x + self.val

        def user_fn(impls: List[InterfaceType], idx: int, val: torch.Tensor) -> torch.Tensor:
            return impls[idx].run(val)

        user_fn_jit = torch.jit.script(user_fn)

        impls = [Impl1(), torch.jit.script(Impl2())]
        val = torch.rand(4, 4)
        user_fn_jit(impls, 0, val)
        user_fn_jit(impls, 1, val)
    """
    warnings.warn(
        "`torch.jit.interface` is deprecated. Please use `torch.compile` instead.",
        DeprecationWarning,
    )
    if not inspect.isclass(obj):
        raise RuntimeError("interface must be applied to a class")
    if not _is_new_style_class(obj):
        raise RuntimeError("TorchScript interfaces must inherit from 'object'")

    # Expected MRO is:
    #   User module
    #   torch.nn.modules.module.Module
    #   object
    is_module_interface = issubclass(obj, torch.nn.Module) and len(obj.mro()) == 3

    if not is_module_interface and len(obj.mro()) > 2:
        raise RuntimeError(
            "TorchScript interface does not support inheritance yet. "
            "Please directly inherit from 'object' or 'nn.Module'."
        )

    qualified_name = _qualified_name(obj)
    rcb = _jit_internal.createResolutionCallbackFromFrame(1)
    # if this type is a `nn.Module` subclass, generate a module interface type
    # instead of a class interface type; a module interface type only compiles
    # the user provided methods as part of the interface
    ast = get_jit_class_def(obj, obj.__name__)
    mangled_classname = torch._C._jit_script_interface_compile(
        qualified_name, ast, rcb, is_module_interface
    )
    obj.__torch_script_interface__ = mangled_classname
    return obj

