
def _shape_as_tensor(self: list[int]) -> list[int]:
    return [len(self)]


def _shape_as_tensor(g: jit_utils.GraphContext, input):
    return g.op("Shape", input)

