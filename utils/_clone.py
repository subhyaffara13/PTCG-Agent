
def _clone(t):
    requires_grad = t.requires_grad
    return t.detach().clone().requires_grad_(requires_grad)

