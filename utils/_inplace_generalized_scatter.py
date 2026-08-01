
def _inplace_generalized_scatter(
    inp: torch.Tensor, src: torch.Tensor, view_ops: list[ViewOp]
) -> torch.Tensor:
    tmp = inp
    for view in view_ops:
        fake_args, fake_kwargs = pytree.tree_map(
            lambda node: node.meta["val"] if isinstance(node, torch.fx.Node) else node,
            (view.args, view.kwargs),
        )
        # slice and select can allocate new unbacked symints, but those won't be reflected
        # in the output of this function, hence shall be ignored.
        fake_mode = detect_fake_mode(fake_args)
        with (
            fake_mode.shape_env.ignore_fresh_unbacked_symbols()
            if fake_mode and fake_mode.shape_env
            else nullcontext()
        ):
            tmp = view.target(tmp, *fake_args, **fake_kwargs)
    try:
        tmp.copy_(src)
    except RuntimeError as e:
        raise RuntimeError(
            f"shape error in scatter op, can not broadcast {src.shape} to {tmp.shape}"
        ) from e
    return inp

