
def find_always_defined_attributes(
    blocks: list[BasicBlock],
    self_reg: Register,
    all_attrs: set[str],
    maybe_defined: AnalysisResult[str],
    maybe_undefined: AnalysisResult[str],
    dirty: AnalysisResult[None],
) -> set[str]:
    """Find attributes that are always initialized in some basic blocks.

    The analysis results are expected to be up-to-date for the blocks.

    Return a set of always defined attributes.
    """
    attrs = all_attrs.copy()
    for block in blocks:
        for i, op in enumerate(block.ops):
            # If an attribute we *read* may be undefined, it isn't always defined.
            if isinstance(op, GetAttr) and op.obj is self_reg:
                if op.attr in maybe_undefined.before[block, i]:
                    attrs.discard(op.attr)
            # If an attribute we *set* may be sometimes undefined and
            # sometimes defined, don't consider it always defined. Unlike
            # the get case, it's fine for the attribute to be undefined.
            # The set operation will then be treated as initialization.
            if isinstance(op, SetAttr) and op.obj is self_reg:
                if (
                    op.attr in maybe_undefined.before[block, i]
                    and op.attr in maybe_defined.before[block, i]
                ):
                    attrs.discard(op.attr)
            # Treat an op that might run arbitrary code as an "exit"
            # in terms of the analysis -- we can't do any inference
            # afterwards reliably.
            if dirty.after[block, i]:
                if not dirty.before[block, i]:
                    attrs = attrs & (
                        maybe_defined.after[block, i] - maybe_undefined.after[block, i]
                    )
                break
            if isinstance(op, ControlOp):
                for target in op.targets():
                    # Gotos/branches can also be "exits".
                    if not dirty.after[block, i] and dirty.before[target, 0]:
                        attrs = attrs & (
                            maybe_defined.after[target, 0] - maybe_undefined.after[target, 0]
                        )
    return attrs

