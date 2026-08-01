
def alias(a: TensorLikeType) -> TensorLikeType:
    return prims.view_of(a)


def alias(g: jit_utils.GraphContext, self):
    return self

