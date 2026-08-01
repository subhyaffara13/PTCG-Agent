
def prepare_softmax_pattern(x, dim):
    xmax = x.amax(dim=dim, keepdim=True)
    xsub = x - xmax
    xexp = xsub.exp()
    xsum = xexp.sum(dim=dim, keepdim=True)
    return xmax, xsum, xsub, xexp

