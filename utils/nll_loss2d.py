
def nll_loss2d(
    g: jit_utils.GraphContext, self, target, weight, reduction, ignore_index
):
    return nll_loss(g, self, target, weight, reduction, ignore_index)

