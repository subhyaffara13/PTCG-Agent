
def simple_map(xs, y0, y1):
    def f(x, y0, y1):
        return inner_f(x, y0, y1)

    return map(f, xs, y0, y1)

