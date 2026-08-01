
def _create_wrapped_callback(
    compiler_fn: CompilerFn,
) -> convert_frame.CatchErrorsWrapper:
    hooks = Hooks()
    return convert_frame.catch_errors_wrapper(
        convert_frame.convert_frame(  # type: ignore[arg-type]
            compiler_fn,
            hooks,
        ),
        hooks,
    )

