
def softshrink(a: TensorLikeType, lambd: float = 0.5):
    # Formula for reference,
    # softshrink(x) = x - lambd if x > lambd
    #               = x + lambd if x < -lambd
    #               = 0 otherwise
    torch._check(
        0 <= lambd <= torch.finfo(a.dtype).max,
        lambda: f"lambda must be in range [0, {torch.finfo(a.dtype).max}] for input dtype {a.dtype}, but found {lambd}",
    )
    # We implement this in one torch.where to generate better code in the backward
    # see https://github.com/pytorch/pytorch/pull/107052#discussion_r1293748211
    # We multiply by 0 for dealing with nans
    return torch.where(torch.abs(a) > lambd, a - torch.sign(a) * lambd, a * 0)


def softshrink(g: jit_utils.GraphContext, self, lambd):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    lambd_op = g.op(
        "Constant",
        value_t=torch.tensor(lambd, dtype=scalar_type.dtype()),
    )
    gt_cond = gt(g, self, lambd_op)
    gt_out = g.op(
        "Where",
        gt_cond,
        sub(g, self, lambd_op),
        g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=scalar_type.dtype()),
        ),
    )
    lt_cond = lt(g, self, neg(g, lambd_op))
    lt_out = g.op(
        "Where",
        lt_cond,
        add(g, self, lambd_op),
        g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=scalar_type.dtype()),
        ),
    )
    return add(g, gt_out, lt_out)

