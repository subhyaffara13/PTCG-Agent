
def build_fingerprint_with_pytree(
    tx: "InstructionTranslator",
    fn_args_vt: Any,
    kwargs: dict[str, Any],
) -> InputFingerprint:
    """Build fingerprint via pytree flatten for nested/kwargs cases."""
    from torch._dynamo.variables.builder import SourcelessBuilder
    from torch._dynamo.variables.higher_order_ops import _make_inlined

    container_vt = SourcelessBuilder.create(tx, (list(fn_args_vt), kwargs))
    flat_list_vt, treespec_vt = _make_inlined(tx, pytree.tree_flatten)(
        container_vt
    ).unpack_var_sequence(tx)
    treespec = treespec_vt.as_python_constant()

    flat_vts: list[tuple[InputTag, VariableTracker]] = []
    arg_sources: list[Source | None] = []
    has_unknown = False

    for vt in flat_list_vt.unpack_var_sequence(tx):
        tag = classify_vt(vt)
        if tag is not None:
            flat_vts.append((tag, vt))
        else:
            has_unknown = True
            continue

        # Always append (even None) to keep positional alignment with flat_vts.
        arg_sources.append(getattr(vt, "source", None))

    return InputFingerprint(flat_vts, arg_sources, has_unknown, treespec)

