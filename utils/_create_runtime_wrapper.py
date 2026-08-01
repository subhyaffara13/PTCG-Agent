
def _create_runtime_wrapper(
    compiled_fn: Callable[..., Any],
    *,
    runtime_metadata: ViewAndMutationMeta,
    indices_of_inps_to_detach: list[int],
    trace_joint: bool,
    keep_input_mutations: bool,
    disable_amp: bool,
) -> Callable[..., Any]:
    compiled_invoker = _RuntimeCompiledFnInvoker(
        compiled_fn=compiled_fn,
        indices_of_inps_to_detach=indices_of_inps_to_detach,
        trace_joint=trace_joint,
        disable_amp=disable_amp,
    )
    runtime_epilogue = _RuntimeForwardEpilogue(
        runtime_metadata=runtime_metadata,
        trace_joint=trace_joint,
        keep_input_mutations=keep_input_mutations,
    )

    def record_runtime_wrapper_prologue_enter() -> AbstractContextManager[None] | None:
        if (
            torch.autograd.profiler._is_profiler_enabled
            and dynamo_config.record_runtime_overhead
        ):
            cm = torch._C._profiler._RecordFunctionFast(
                "AOTDispatcher Runtime Wrapper Prologue"
            )
            cm.__enter__()
            return cm
        return None

    def record_runtime_wrapper_prologue_exit(
        cm: AbstractContextManager[None] | None,
    ) -> None:
        if cm is not None:
            cm.__exit__(None, None, None)

    @simple_wraps(compiled_invoker.compiled_fn)
    def runtime_wrapper(args: list[Any]) -> Any:
        # Create context manager for profiler
        cm = record_runtime_wrapper_prologue_enter()
        prologue_exited = False

        def exit_prologue() -> None:
            nonlocal prologue_exited
            if not prologue_exited:
                record_runtime_wrapper_prologue_exit(cm)
                prologue_exited = True

        try:
            # stash a ref to each input tensor we plan to use after the compiled function
            orig_inputs = runtime_epilogue.capture_orig_inputs(args)
            runtime_epilogue.increment_mutation_versions(args)
            all_outs = compiled_invoker.run(args, on_before_call=exit_prologue)
        finally:
            exit_prologue()

        del args
        return runtime_epilogue.finalize(orig_inputs, all_outs)

    if not (trace_joint and _should_disable_saved_tensors_hooks()):
        return runtime_wrapper

    # Disabling saved tensors hooks
    @simple_wraps(runtime_wrapper)
    def _runtime_wrapper(*args: Any, **kwargs: Any) -> Any:
        with _disable_saved_tensors_hooks():
            return runtime_wrapper(*args, **kwargs)

    return _runtime_wrapper

