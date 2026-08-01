
def reshape_as(self: TensorLikeType, other: TensorLikeType) -> TensorLikeType:
    return self.reshape(other.size())


def reshape_as(g: jit_utils.GraphContext, self, other):
    shape = g.op("Shape", other)
    return reshape(g, self, shape)

