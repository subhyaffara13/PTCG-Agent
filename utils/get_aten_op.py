from typing import Callable

def get_aten_op(fn: Callable, name: str):
    """
    Given the __module__ of reference and its name, it returns
    (our best guess of) the ATen name of the associated operation

    Note: In ATen, the __name__ of a function within a module often
    starts by the module name. E.g. linalg_eigh, or special_zeta
    """
    module = fn.__module__
    prefix = "torch._refs"
    if not module.startswith(prefix):
        raise AssertionError(f"module must start with {prefix}, got {module}")
    module = module[len(prefix) :]
    # We want to go from .special / .nn.functional
    # to special and special_ / nn_functional_
    if module:
        module = module[1:]
        module = module.replace(".", "_")
        module = module + "_"
    return getattr(torch._ops.ops.aten, f"{module}{name}")

