
def prim_unchecked_cast(g: jit_utils.GraphContext, self):
    # exists to refine the type of the Value
    # if x is Optional[Tensor], unchecked_cast will cast
    # x to Tensor, so the rest of the graph knows that x is a Tensor.
    if isinstance(self.type(), _C.OptionalType):
        return g.op("OptionalGetElement", self)

    return self


def prim_unchecked_cast(g: jit_utils.GraphContext, self):
    return self

