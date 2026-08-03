from typing import Callable
import math


def _get_sym_math_fn(name):
    def fn(a):
        if overrides.has_torch_function_unary(a):
            return overrides.handle_torch_function(fn, (a,), a)
        if isinstance(a, SymInt):
            a = torch.sym_float(a)
        if hasattr(a, f"__sym_{name}__"):
            return getattr(a, f"__sym_{name}__")()
        return getattr(math, name)(a)

    return fn


def _get_sym_math_fn(name: str) -> Callable[[sympy.Basic], sympy.Basic]:
    def fn(a: sympy.Basic) -> sympy.Basic:
        import torch.utils._sympy.functions

        return getattr(torch.utils._sympy.functions, f"OpaqueUnaryFn_{name}")(a)

    return fn

