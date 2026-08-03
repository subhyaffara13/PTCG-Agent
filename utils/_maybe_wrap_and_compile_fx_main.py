import functools
from typing import Any, Callable

def _maybe_wrap_and_compile_fx_main(
    model_: GraphModule,
    example_inputs_: Sequence[InputType],
    inner_compile: Callable[..., OutputCode],
    ignore_shape_env: bool,
    *,
    get_decomp_fn: Callable[..., dict[Any, Callable[..., Any]]] = select_decomp_table,
    compile_region_name: str | None = None,
) -> CompileFxOutput:
    """
    Part of compile_fx, called after patching configs.

    Ultimately we want to call _compile_fx_main, where the actual work happens.
    But under various conditions, various forms of wrapping might be needed
    around _compile_fx_main.
    """
    # Each wrapper below takes a self-contained compile_gm function which is
    # called inside the wrapper. This just recursively calls this function.
    compile_gm = functools.partial(
        _maybe_wrap_and_compile_fx_main,
        inner_compile=inner_compile,
        ignore_shape_env=ignore_shape_env,
        get_decomp_fn=get_decomp_fn,
        compile_region_name=compile_region_name,
    )
    if not graph_returns_tuple(model_):
        return make_graph_return_tuple(model_, example_inputs_, compile_gm)

    if isinstance(model_, GraphModule) and isinstance(
        model_.graph._codegen, _PyTreeCodeGen
    ):
        # this graph is the result of dynamo.export()
        return handle_dynamo_export_graph(model_, example_inputs_, compile_gm)

    if any(isinstance(x, (list, tuple, dict)) for x in example_inputs_):
        # NB: this short circuit never occurs for Dynamo produced graphs
        # (which are pre-flattened)
        return flatten_graph_inputs(model_, example_inputs_, compile_gm)

    # Finally do the actual work!
    return _compile_fx_main(
        model_,
        example_inputs_,
        inner_compile,
        ignore_shape_env,
        get_decomp_fn=get_decomp_fn,
        compile_region_name=compile_region_name,
    )

