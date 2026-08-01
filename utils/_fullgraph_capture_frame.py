
def _fullgraph_capture_frame(
    frame: FrameInfo,
    *,
    constraints: list[Constraint] | None = None,
    _is_export_deprecated_do_not_use: bool = False,
) -> CaptureOutput:
    from torch._guards import TracingContext

    backend_input: BackendInput | None = None

    def fullgraph_compiler(
        gm: torch.fx.GraphModule, example_inputs: list[torch.Tensor]
    ) -> torch.fx.GraphModule:
        nonlocal backend_input
        tracing_context = TracingContext.get()
        fake_mode = tracing_context.fake_mode
        tensor_to_context = tracing_context.tensor_to_context
        assert fake_mode is not None
        assert isinstance(gm.meta["backend_id"], str)
        backend_input = BackendInput(
            gm.meta["backend_id"], gm, example_inputs, fake_mode, tensor_to_context
        )
        return gm

    try:
        dynamo_output = compile_frame(
            frame.code,
            frame.globals,
            frame.locals,
            frame.builtins,
            frame.closure,
            compiler_fn=fullgraph_compiler,
            export=_is_export_deprecated_do_not_use,
            export_constraints=constraints,  # type: ignore[arg-type]
            one_graph=True,
            restart_reasons=set(),
        )
        # https://github.com/pytorch/pytorch/blob/main/torch/_dynamo/eval_frame.py#L831
    except (Unsupported, UncapturedHigherOrderOpError, UserError) as e:
        augment_exc_message(e)
        if config.verbose:
            raise
        # strip internal tracebacks from causes
        cur_exn: BaseException = e
        while cur_exn.__cause__ is not None:
            cur_exn.__cause__.with_traceback(None)
            cur_exn = cur_exn.__cause__

        raise e.with_traceback(None) from e.__cause__  # User compiler error

    return CaptureOutput(
        dynamo_output.graph_capture_output(frame.argdefs, frame.kwdefaults),
        backend_input,
    )

