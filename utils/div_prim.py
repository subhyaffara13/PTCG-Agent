import math


def div_prim(a, b):
    is_integral = all(is_boolean_type(x) or is_integer_type(x) for x in [a, b])

    if is_integral:
        return truncdiv(a, b)

    # Disable CPU optimization to avoid precision issues.
    # see https://github.com/pytorch/pytorch/issues/157959
    if (divisor := get_constant_value(b)) is not None and a.get_device().type != "cpu":
        # Replace divide by constant with multiply by reciprocal

        if divisor.value == 0:
            reciprocal = math.copysign(float("inf"), divisor.value)
        else:
            reciprocal = 1.0 / divisor.value
        return mul(a, reciprocal)

    def fn(*args):
        return ops.truediv(*args)

    return make_pointwise(fn)(a, b)

