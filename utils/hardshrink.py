
def hardshrink(a: TensorLikeType, lambd: float = 0.5):
    # Formula for reference,
    # hardshrink(x) = x if x > lambd
    #               = x if x < -lambd
    #               = 0 otherwise
    return torch.where(torch.abs(a) <= lambd, 0, a)


def hardshrink(g: jit_utils.GraphContext, self, lambd):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    lambd_op = g.op(
        "Constant",
        value_t=torch.tensor(lambd, dtype=scalar_type.dtype()),
    )
    cond = logical_or(g, gt(g, self, lambd_op), lt(g, self, neg(g, lambd_op)))
    return g.op(
        "Where",
        cond,
        self,
        g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=scalar_type.dtype()),
        ),
    )

