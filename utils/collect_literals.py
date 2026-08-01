
def collect_literals(fn: FuncIR, literals: Literals) -> None:
    """Store all Python literal object refs in fn.

    Collecting literals must happen only after we have the final IR.
    This way we won't include literals that have been optimized away.
    """
    for block in fn.blocks:
        for op in block.ops:
            if isinstance(op, LoadLiteral):
                literals.record_literal(op.value)

