
def nested_map(xs, y0, y1):
    def f1(xx, y0, y1):
        def f2(x, y0, y1):
            return inner_f(x, y0, y1)

        return map(f2, xx, y0, y1)

    return map(f1, xs, y0, y1)

