
def dynamo_graph_capture_for_export(
    fn: Callable[..., Any],
    constraints: list[Constraint] | None = None,
) -> Callable[..., Any]:
    if isinstance(fn, torch._ops.OpOverload):

        def default_annotation(arg: torch.Argument) -> str:
            if arg.has_default_value():
                return f"={arg.default_value!r}"
            return ""

        has_kwarg_only = False
        arg_list = []
        for arg in fn._schema.arguments:
            if arg.kwarg_only and not has_kwarg_only:
                has_kwarg_only = True
                arg_list.append("*")
            arg_list.append(arg.name + default_annotation(arg))
        func_str = f"""
def op_overload_wrapper({", ".join(arg_list)}):
    return op({", ".join([f"{arg.name}={arg.name}" for arg in fn._schema.arguments])})
"""
        out = {}
        exec(func_str, {"op": fn}, out)
        fn = out["op_overload_wrapper"]  # type: ignore[assignment]

    def inner(*args: Any, **kwargs: Any) -> Any:
        assert not torch._dynamo.config.install_free_tensors
        with (
            _compiling_state_context(),
            torch._dynamo.config.patch(
                replay_side_effects=False, side_effect_replay_policy="warn"
            ),
            get_metrics_context(),
            dynamo_timed("fullgraph_capture"),
        ):
            out = fullgraph_capture(
                fn,
                args,
                kwargs,
                constraints=constraints,
            )
        graph_module = create_fx_graph_from_captured_output(out, fn, args, kwargs)
        return graph_module

    return inner

