
def print_compile(fx_g: fx.GraphModule, _: Any) -> fx.GraphModule:
    print(fx_g.code)
    return fx_g

