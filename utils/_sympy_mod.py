
def _sympy_mod(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import Mod, PythonMod

    if a.is_nonnegative and b.is_nonnegative:
        return Mod(a, b)
    else:
        return PythonMod(a, b)

