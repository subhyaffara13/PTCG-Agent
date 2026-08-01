
def inductor_accuracy_fails(
    fx_g: torch.fx.GraphModule,
    args: Sequence[Any],
    check_str: str | None = None,
    *,
    require_fp64: bool = False,
    ignore_non_fp: bool = False,
) -> bool:
    from torch._inductor.compile_fx import compile_fx_inner

    return backend_aot_accuracy_fails(
        fx_g,
        args,  # type: ignore[arg-type]
        compile_fx_inner,  # type: ignore[arg-type]
        require_fp64=require_fp64,
        ignore_non_fp=ignore_non_fp,
    )

