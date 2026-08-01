
def simple_invoke_quant(x):
    def fn(x, y):
        return (torch.sin(x) * y,)

    return quant_tracer(fn, x, x)[0] * 2.0

