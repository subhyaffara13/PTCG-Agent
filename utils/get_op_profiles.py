
def get_op_profiles(
    gm: torch.fx.GraphModule, ops_to_guard: set[str]
) -> dict[str, set[OpProfile]]:
    """
    This is used by draft_export to get a list of custom operator profiles so
    that we can generate fake kernels.
    """

    def _get_op_profile(node: torch.fx.Node) -> OpProfile:
        args_profile = tuple(
            TensorMetadata.maybe_from_tensor(arg.meta.get("val"))
            if isinstance(arg, torch.fx.Node)
            else None
            for arg in (*node.args, *node.kwargs.values())
        )

        out_profile = None
        meta = node.meta.get("val")
        if meta is None:
            raise AssertionError("node.meta['val'] must not be None")
        if isinstance(meta, torch.Tensor):
            out_profile = TensorMetadata.maybe_from_tensor(meta)
        elif isinstance(meta, (list, tuple)):
            out_profile = tuple(TensorMetadata.maybe_from_tensor(m) for m in meta)  # type: ignore[assignment]
        if out_profile is None:
            raise AssertionError(
                f"out_profile must not be None for meta type {type(meta)}"
            )

        return OpProfile(args_profile, out_profile)  # type: ignore[arg-type]

    op_profiles: dict[str, set[OpProfile]] = defaultdict(set)

    for node in gm.graph.nodes:
        if node.op == "call_function" and str(node.target) in ops_to_guard:
            op_profiles[str(node.target)].add(_get_op_profile(node))

    return op_profiles

