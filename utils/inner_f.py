
def inner_f(x, y0, y1):
    return [x[0].cos().add_(1.0) * y0, (x[1] + y1.sin()).cos_().view(x[1].size())]

