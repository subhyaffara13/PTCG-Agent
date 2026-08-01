
def simple_ts_compile(fx_g: fx.GraphModule, _: Any) -> torch.jit.ScriptModule:
    strip_overloads(fx_g)
    f = torch.jit.script(fx_g)
    f = torch.jit.freeze(f.eval())
    return f

