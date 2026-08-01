
def _find_default_argument(name: str, blocks: list[BasicBlock]) -> object:
    # Find assignment inserted by gen_arg_defaults. Assumed to be the first assignment.
    for block in blocks:
        for op in block.ops:
            if isinstance(op, Assign) and op.dest.name == name:
                return _extract_python_literal(op.src)
    return _NOT_REPRESENTABLE

