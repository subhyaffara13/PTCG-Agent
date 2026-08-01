
def simple_invoke_quant_packed(x):
    def fn(x):
        return (torch.sin(x),)

    return invoke_quant_packed(fn, x)[0] * 2.0

