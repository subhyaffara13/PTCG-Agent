
def maybe_append_dec_ref(
    ops: list[Op], dest: Value, defined: AnalysisDict[Value], key: tuple[BasicBlock, int]
) -> None:
    if dest.type.is_refcounted and not isinstance(dest, (Integer, Undef)):
        ops.append(DecRef(dest, is_xdec=is_maybe_undefined(defined[key], dest)))

