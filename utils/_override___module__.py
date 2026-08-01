
def _override___module__():
    namespace_names = globals()
    for ufunc_name in [
        'absolute', 'arccos', 'arccosh', 'add', 'arcsin', 'arcsinh', 'arctan',
        'arctan2', 'arctanh', 'bitwise_and', 'bitwise_count', 'invert',
        'left_shift', 'bitwise_or', 'right_shift', 'bitwise_xor', 'cbrt',
        'ceil', 'conjugate', 'copysign', 'cos', 'cosh', 'deg2rad', 'degrees',
        'divide', 'divmod', 'equal', 'exp', 'exp2', 'expm1', 'fabs',
        'float_power', 'floor', 'floor_divide', 'fmax', 'fmin', 'fmod',
        'frexp', 'gcd', 'greater', 'greater_equal', 'heaviside', 'hypot',
        'isfinite', 'isinf', 'isnan', 'isnat', 'lcm', 'ldexp', 'less',
        'less_equal', 'log', 'log10', 'log1p', 'log2', 'logaddexp',
        'logaddexp2', 'logical_and', 'logical_not', 'logical_or',
        'logical_xor', 'matmul', 'matvec', 'maximum', 'minimum', 'remainder',
        'modf', 'multiply', 'negative', 'nextafter', 'not_equal', 'positive',
        'power', 'rad2deg', 'radians', 'reciprocal', 'rint', 'sign', 'signbit',
        'sin', 'sinh', 'spacing', 'sqrt', 'square', 'subtract', 'tan', 'tanh',
        'trunc', 'vecdot', 'vecmat',
    ]:
        ufunc = namespace_names[ufunc_name]
        ufunc.__module__ = "numpy"
        ufunc.__qualname__ = ufunc_name


def _override___module__():
    for ufunc in [
        isalnum, isalpha, isdecimal, isdigit, islower, isnumeric, isspace,
        istitle, isupper, str_len,
    ]:
        ufunc.__module__ = "numpy.strings"
        ufunc.__qualname__ = ufunc.__name__

