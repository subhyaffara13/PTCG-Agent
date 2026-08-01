
def view_as(self: TensorLikeType, other: TensorLikeType) -> TensorLikeType:
    return self.view(other.size())


def view_as(g: jit_utils.GraphContext, self, other):
    shape = g.op("Shape", other)
    return reshape(g, self, shape)

