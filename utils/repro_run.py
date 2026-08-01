
def repro_run(options: Any, mod: nn.Module, load_args: Any) -> None:
    from torch._inductor.compile_fx import compile_fx_inner

    mod, args = repro_common(options, mod, load_args)

    from torch.cuda import synchronize

    compiled = compile_fx_inner(mod, args)
    assert not isinstance(compiled, str)

    if options.accuracy != "":
        # We don't really respect --accuracy vs --strict-accuracy here, it
        # seems counterintuitive
        if not same_two_models(
            mod,
            compiled,  # type: ignore[arg-type]
            args,
            only_fwd=True,
            ignore_non_fp=config.repro_ignore_non_fp,
        ):
            raise AccuracyError("Bad accuracy detected")
    else:
        need_sync = False

        for arg in args:
            if isinstance(arg, torch.Tensor) and arg.is_cuda:
                need_sync = True
                break

        compiled(list(args))

        if need_sync:
            synchronize()  # ensure segfaults are surfaced


def repro_run(options: Any, mod: torch.nn.Module, load_args: Any) -> None:
    opt_mod = torch._dynamo.optimize(options.backend)(mod)

    if options.accuracy != "":
        mod.eval()
        opt_mod.eval()  # type: ignore[union-attr]

        with torch.amp.autocast("cuda", enabled=options.autocast):
            # TODO: disable clone
            args = run_load_args(options, mod, load_args)
            assert same_two_models(mod, mod, args), "Eager itself failed"  # type: ignore[arg-type]
            if not same_two_models(
                mod,  # type: ignore[arg-type]
                opt_mod,  # type: ignore[arg-type]
                args,
                only_fwd=config.repro_forward_only,
                ignore_non_fp=config.repro_ignore_non_fp,
            ):
                raise AccuracyError("Dynamo failed")
    else:
        with torch.amp.autocast("cuda", enabled=options.autocast):
            args = run_load_args(options, mod, load_args)
            run_fwd_maybe_bwd(mod, args, only_fwd=options.only_fwd, disable_clone=True)  # type: ignore[arg-type]
            del args

            args = run_load_args(options, mod, load_args)
            run_fwd_maybe_bwd(
                opt_mod,  # type: ignore[arg-type]
                args,
                only_fwd=options.only_fwd,
                disable_clone=True,  # type: ignore[arg-type]
            )


def repro_run(
    options: Any,
    exported_program: ExportedProgram,
    config_patches: dict[str, Any] | None,
) -> None:
    from torch._inductor import _aoti_compile_and_package_inner

    gm, args, kwargs = repro_common(options, exported_program)

    from torch.cuda import synchronize

    _aoti_compile_and_package_inner(
        gm,
        args,
        kwargs,
        load_and_run=True,
        check_accuracy=options.accuracy,
        inductor_configs=config_patches,
    )

    need_sync = False

    for arg in args:
        if isinstance(arg, torch.Tensor) and arg.is_cuda:
            need_sync = True
            break

    if need_sync:
        synchronize()  # ensure segfaults are surfaced

