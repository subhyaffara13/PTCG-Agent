
def numel(sizes: list[int]):
    numel = 1
    for elem in sizes:
        numel *= elem
    return numel


def numel(g: jit_utils.GraphContext, self):
    return symbolic_helper._numel_helper(g, self)

