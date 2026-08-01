
def backend_fails(
    gm: fx.GraphModule,
    example_inputs: Sequence[Any],
    compiler_fn: CompilerFn,
    orig_failure: Sequence[Any],
) -> bool:
    """
    Minifier uses this function to identify if the minified graph module fails
    with the same error.

    One caveat is that minifier can potentially go into a wrong direction when
    the resulting graph module fails for a different reason. To avoid this, we
    save the string for the original exception and check similarity between new
    and old exception. They can be somewhat different in some cases, when the
    exception string depends on the failing node information. So, we have a
    loose similarity metric to guide the minifier path.
    """
    from difflib import SequenceMatcher

    try:
        # Run the original gm to check eager validity
        run_fwd_maybe_bwd(gm, clone_inputs_retaining_gradness(example_inputs))
        compiled_gm = compiler_fn(gm, example_inputs)  # type: ignore[arg-type]
        run_fwd_maybe_bwd(compiled_gm, clone_inputs_retaining_gradness(example_inputs))  # type: ignore[arg-type]
    except Exception as e:
        new_failure = str(e)
        if SequenceMatcher(None, orig_failure, new_failure).ratio() > 0.5:
            return True
    return False

