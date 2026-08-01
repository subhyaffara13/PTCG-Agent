
def test_sympy__functions__special__singularity_functions__SingularityFunction():
    from sympy.functions.special.singularity_functions import SingularityFunction
    assert _test_args(SingularityFunction(x, y, z))

