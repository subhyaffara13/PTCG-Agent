
def levin(ctx, method = "levin", variant = "u"):
    L = levin_class(method = method, variant = variant)
    L.ctx = ctx
    return L

