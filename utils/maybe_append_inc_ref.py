
def maybe_append_inc_ref(ops: list[Op], dest: Value) -> None:
    if dest.type.is_refcounted:
        ops.append(IncRef(dest))

