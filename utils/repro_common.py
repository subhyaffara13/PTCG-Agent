
def repro_common(
    options: Any, mod: nn.Module, load_args: Any
) -> tuple[torch.fx.GraphModule, list[Any]]:
    # Invariant for graphs we generate with the repro script
    assert not any(mod.named_parameters())
    for n, b in mod.named_buffers():
        if b.numel() > MAX_CONSTANT_NUMEL_INLINE:
            log.warning(
                "Constant %s was not serialized, generated random data instead. "
                "If you think this is affecting you, please comment on "
                "https://github.com/pytorch/pytorch/issues/100468",
                n,
            )

    if not hasattr(load_args, "_version"):
        log.warning(
            "load_args does not have a _version attribute, please file a bug to PyTorch "
            "and describe how you generate this repro script"
        )
    else:
        if load_args._version > 0:
            log.warning(
                "load_args is version %s, but this version of PyTorch only supports "
                "version 0.  We will try to run it anyway but there may be an incompatibility; "
                "if so, try upgrading your version of PyTorch.",
                load_args._version,
            )

    nop_reader = NopInputReader()
    load_args(nop_reader)

    with tqdm(desc="Loading inputs", total=nop_reader.total) as pbar:
        input_reader = InputReader(save_dir=options.save_dir, pbar=pbar)
        load_args(input_reader)
        args = input_reader.args

    # Turn mod into a GraphModule the slow way
    # TODO: speed this up
    mod = make_fx(mod, tracing_mode=options.tracing_mode)(*args)

    # pyrefly: ignore [bad-assignment]
    torch._inductor.config.generate_intermediate_hooks = True

    return mod, args


def repro_common(
    options: Any, exported_program: ExportedProgram
) -> tuple[torch.fx.GraphModule, Any, Any]:
    # pyrefly: ignore [bad-assignment]
    torch._inductor.config.generate_intermediate_hooks = True
    mod = exported_program.module(check_guards=False)
    args, kwargs = exported_program.example_inputs
    return mod, args, kwargs  # type: ignore[return-value]

