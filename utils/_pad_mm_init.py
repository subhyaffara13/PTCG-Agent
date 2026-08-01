
def _pad_mm_init(input_device: torch.device | None = None) -> None:
    from .joint_graph import patterns

    if input_device:
        device = str(input_device)
    else:
        if torch.cuda.is_available():
            # workaround https://github.com/pytorch/pytorch/issues/97894
            device = "cuda"
        elif torch.xpu.is_available():
            device = "xpu"
        else:
            device = "cpu"

    # sizes/values dont actually matter for initial trace
    # once we get a possible match we re-trace with the actual values and verify the match still holds

    dim2a = functools.partial(torch.empty, (4, 4), device=device, requires_grad=True)
    dim2b = functools.partial(torch.empty, (4, 4), device=device, requires_grad=True)

    dim3a = functools.partial(torch.empty, (4, 4, 4), device=device, requires_grad=True)
    dim3b = functools.partial(torch.empty, (4, 4, 4), device=device, requires_grad=True)

    dim1a = functools.partial(torch.empty, (4), device=device, requires_grad=True)

    # workaround https://github.com/pytorch/pytorch/issues/97894
    # 0.113377 is a "magic" value that lets us recover the lost input arg relationship
    rep = {"beta": 0.213377, "alpha": 0.113377}

    for pattern, replacement, args, workaround, extra_check in [
        (
            typing.cast(SearchFn, mm_pattern),
            typing.cast(ReplaceFn, mm_replace),
            [dim2a(), dim2b()],
            {},
            should_pad_mm,
        ),
        (
            typing.cast(SearchFn, bmm_pattern),
            typing.cast(ReplaceFn, bmm_replace),
            [dim3a(), dim3b()],
            {},
            should_pad_bmm,
        ),
        (
            typing.cast(SearchFn, addmm_pattern),
            typing.cast(ReplaceFn, addmm_replace),
            [dim1a(), dim2a(), dim2b()],
            rep,
            should_pad_addmm,
        ),
    ]:
        assert isinstance(workaround, dict)  # mypy is unable to infer the type properly
        name = pattern.__name__

        gen_register_replacement(
            f"{name}_training",
            pattern,
            replacement,
            args,
            # pyrefly: ignore [bad-argument-type]
            joint_fwd_bwd,
            # pyrefly: ignore [bad-argument-type]
            patterns,
            extra_check=extra_check,
            scalar_workaround=workaround,
            skip_duplicates=True,
        )

        gen_register_replacement(
            f"{name}_inference",
            pattern,
            replacement,
            args,
            # pyrefly: ignore [bad-argument-type]
            fwd_only,
            # pyrefly: ignore [bad-argument-type]
            patterns,
            extra_check=extra_check,
            scalar_workaround=workaround,
            skip_duplicates=True,
        )

