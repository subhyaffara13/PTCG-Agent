
def aminmax(self, *, dim=None, keepdim=False):
    # pyrefly: ignore [bad-argument-type]
    amin = torch.amin(self, dim=dim, keepdim=keepdim)
    # pyrefly: ignore [bad-argument-type]
    amax = torch.amax(self, dim=dim, keepdim=keepdim)
    return amin, amax


def aminmax(g: jit_utils.GraphContext, self, dim, keepdim):
    if not symbolic_helper._is_none(dim):
        dim = symbolic_helper._get_const(dim, "i", "dim")
        axes = g.op("Constant", value_t=torch.tensor([dim], dtype=torch.long))
        return g.op("ReduceMin", self, axes, keepdims_i=keepdim), g.op(
            "ReduceMax", self, axes, keepdims_i=keepdim
        )
    else:
        return g.op("ReduceMin", self, keepdims_i=keepdim), g.op(
            "ReduceMax", self, keepdims_i=keepdim
        )


def aminmax(g: jit_utils.GraphContext, self, dim, keepdim):
    reduce_kwargs = {"keepdims_i": keepdim}
    if not symbolic_helper._is_none(dim):
        dim = symbolic_helper._get_const(dim, "i", "dim")
        reduce_kwargs["axes_i"] = [dim]

    return g.op("ReduceMin", self, **reduce_kwargs), g.op(
        "ReduceMax", self, **reduce_kwargs
    )

