
def mark_attr_initialization_ops(
    blocks: list[BasicBlock],
    self_reg: Register,
    maybe_defined: AnalysisResult[str],
    dirty: AnalysisResult[None],
) -> None:
    """Tag all SetAttr ops in the basic blocks that initialize attributes.

    Initialization ops assume that the previous attribute value is the error value,
    so there's no need to decref or check for definedness.
    """
    for block in blocks:
        for i, op in enumerate(block.ops):
            if isinstance(op, SetAttr) and op.obj is self_reg:
                attr = op.attr
                if attr not in maybe_defined.before[block, i] and not dirty.after[block, i]:
                    op.mark_as_initializer()

