
def _floor_divide(g: jit_utils.GraphContext, self, other):
    if symbolic_helper._is_fp(self) or symbolic_helper._is_fp(other):
        out = opset9.true_divide(g, self, other)
        return g.op("Floor", out)
    else:
        # Integer division does truncation rounding
        div = g.op("Div", self, other)
        # Division is negative if: self < 0 != other < 0
        zero = g.op("Constant", value_t=torch.tensor(0, dtype=torch.int64))
        negative = g.op("Xor", g.op("Less", self, zero), g.op("Less", other, zero))

        # For negative numbers with self % other != 0, subtract 1 to round down instead of up
        mod = g.op("Mod", self, other, fmod_i=0)
        fixup_mask = g.op("And", negative, g.op("Not", g.op("Equal", mod, zero)))

        one = g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))
        fixup = g.op("Sub", div, one)
        return g.op("Where", fixup_mask, fixup, div)


def _floor_divide(g: jit_utils.GraphContext, self, other):
    if symbolic_helper._is_fp(self) or symbolic_helper._is_fp(other):
        out = true_divide(g, self, other)
        return g.op("Floor", out)
    else:
        # Integer division does truncation rounding
        div = g.op("Div", self, other)
        # Division is negative if: self < 0 != other < 0
        zero = g.op("Constant", value_t=torch.tensor(0, dtype=torch.int64))
        negative = g.op(
            "Xor",
            symbolic_helper._lt_helper(g, self, zero),
            symbolic_helper._lt_helper(g, other, zero),
        )

        # For negative numbers with self % other != 0, subtract 1 to round down instead of up
        mod = g.op("Sub", self, g.op("Mul", div, other))
        fixup_mask = g.op("And", negative, g.op("Not", g.op("Equal", mod, zero)))

        one = g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))
        fixup = g.op("Mul", fixup_mask, one)
        return g.op("Sub", div, fixup)

