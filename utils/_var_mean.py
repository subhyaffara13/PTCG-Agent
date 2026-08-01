
def _var_mean(g: jit_utils.GraphContext, input, *args):
    if len(args) == 1:
        return symbolic_helper._var_mean_helper(g, input, None, args[0], None)
    else:
        return symbolic_helper._var_mean_helper(g, input, *args)


def _var_mean(g: jit_utils.GraphContext, input, dim, correction, keepdim):
    return symbolic_helper._var_mean_helper(g, input, dim, correction, keepdim)

