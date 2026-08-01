
def _div_rounding_mode(g: jit_utils.GraphContext, self, other, rounding_mode):
    if rounding_mode == "floor":
        return _floor_divide(g, self, other)
    else:
        return opset9._div_rounding_mode(g, self, other, rounding_mode)


def _div_rounding_mode(g: jit_utils.GraphContext, self, other, rounding_mode):
    if rounding_mode is None:
        return true_divide(g, self, other)
    elif rounding_mode == "floor":
        return _floor_divide(g, self, other)
    elif rounding_mode == "trunc":
        return _trunc_divide(g, self, other)
    else:
        raise errors.SymbolicValueError(
            f'Unsupported rounding mode: "{rounding_mode}". Expected None, "floor" or "trunc"',
            self,
        )

