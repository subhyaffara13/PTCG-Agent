
def resolve_unbacked_bindings(
    shape_env: ShapeEnv | None,
    bindings: dict[sympy.Symbol, pytree.KeyPath] | None,
) -> dict[sympy.Symbol, pytree.KeyPath] | None:
    """
    When we do fake tensor prop, we oftentimes will allocate new unbacked symints.
    We then run proxy tensor mode, which populates node.meta["unbacked_bindings"]
    with these new symints. To ensure consistency we use PropagateUnbackedSymInts
    to rename unbacked bindings to their old ones. But all of the node metas are
    still using the old bindings from before the renaming. This function helps to
    post facto apply any renamings discovered in the PropagateUnbackedSymInts pass.
    """
    if bindings is None:
        return None
    if shape_env is None:
        raise AssertionError("shape_env should not be None")
    return {shape_env.unbacked_renamings.get(k, k): v for k, v in bindings.items()}

