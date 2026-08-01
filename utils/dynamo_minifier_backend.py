
def dynamo_minifier_backend(
    gm: fx.GraphModule, example_inputs: Sequence[Any], compiler_name: str | None
) -> fx.GraphModule:
    from functorch.compile import minifier

    compiler_fn = lookup_backend(compiler_name)  # type: ignore[arg-type]

    # TODO: It's inconsistent to pass SymInt inputs but REAL tensors.
    # We should pass ints and look at the GraphModule placeholders
    # to resolve them to SymInt (if necessary)
    example_inputs = [
        i.node.hint if isinstance(i, torch.SymInt) else i for i in example_inputs
    ]

    try:
        compiled_gm = compiler_fn(gm, example_inputs)
        run_fwd_maybe_bwd(compiled_gm, example_inputs)  # type: ignore[arg-type]
        raise ValueError("No issue was detected")
    except Exception as exc:
        orig_failure = str(exc)
        log.warning(
            "Compiled Fx GraphModule failed. Creating script to minify the error."
        )
        dump_state_fn = functools.partial(
            dump_backend_state, compiler_name=compiler_name
        )
        dump_state_fn(fx.GraphModule(gm, copy.deepcopy(gm.graph)), example_inputs)
        fails_fn = functools.partial(
            backend_fails,
            compiler_fn=compiler_fn,
            orig_failure=orig_failure,
        )
        minifier(
            gm,
            example_inputs,
            module_fails=fails_fn,
            dump_state=dump_state_fn,
        )
    return gm

