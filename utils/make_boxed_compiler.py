
def make_boxed_compiler(
    compiler: Callable[..., Any],
) -> Callable[..., Any]:
    @wraps(compiler)
    def f(fx_g: Any, inps: Any) -> Any:
        out_f = compiler(fx_g, inps)
        fx_g = make_boxed_func(out_f)
        return fx_g

    return f

