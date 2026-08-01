
def prepare_softmax_replacement(x, dim):
    """
    Return xsub since otherwise log-softmax can not be matched
    due to a use of this intermediate node. Same reason to return
    xsub.exp() for softmax.
    """
    from torch._inductor.inductor_prims import prepare_softmax_online

    xmax, xsum = prepare_softmax_online(x, dim)
    xsub = x - xmax
    return xmax, xsum, xsub, xsub.exp()

