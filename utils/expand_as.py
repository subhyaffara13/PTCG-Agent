
def expand_as(x, y):
    return expand(x, y.get_size())


def expand_as(a: Tensor, b: Tensor) -> Tensor:
    return a.expand(b.shape)


def expand_as(g: jit_utils.GraphContext, self, other):
    self_t = symbolic_helper._maybe_get_const(self, "t")
    if isinstance(self_t, torch.Tensor):
        orig_type = self_t.dtype
        self_t = self_t.to(torch.double)
        dims = []
        for d in range(self_t.dim()):
            if torch.equal(self_t.mean(d).unsqueeze(d).expand_as(self_t), self_t):
                dims.append(d)
                self = g.op(
                    "Constant", value_t=self_t.mean(dims, keepdim=True).to(orig_type)
                )

    shape = g.op("Shape", other)
    return g.op("Expand", self, shape)

