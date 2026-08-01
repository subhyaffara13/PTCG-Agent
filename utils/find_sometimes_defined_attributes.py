
def find_sometimes_defined_attributes(
    blocks: list[BasicBlock],
    self_reg: Register,
    maybe_defined: AnalysisResult[str],
    dirty: AnalysisResult[None],
) -> set[str]:
    """Find attributes that are sometimes initialized in some basic blocks."""
    attrs: set[str] = set()
    for block in blocks:
        for i, op in enumerate(block.ops):
            # Only look at possibly defined attributes at exits.
            if dirty.after[block, i]:
                if not dirty.before[block, i]:
                    attrs = attrs | maybe_defined.after[block, i]
                break
            if isinstance(op, ControlOp):
                for target in op.targets():
                    if not dirty.after[block, i] and dirty.before[target, 0]:
                        attrs = attrs | maybe_defined.after[target, 0]
    return attrs

