
def prim_max(g: jit_utils.GraphContext, self, other):
    return symbolic_helper._op_with_optional_float_cast(
        g, "Max", self, other, opset_before=12
    )

