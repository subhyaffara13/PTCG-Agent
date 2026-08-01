
def has_same_metadata(t1: Tensor, t2: Tensor) -> bool:
    return (
        guard_or_false(sym_eq(t1.size(), t2.size()))
        and guard_or_false(t1.layout == t2.layout)
        and (
            is_sparse_any(t1)
            or (
                guard_or_false(sym_eq(t1.stride(), t2.stride()))
                and guard_or_false(t1.storage_offset() == t2.storage_offset())
            )
        )
        and t1.is_conj() == t2.is_conj()
        and t1.is_neg() == t2.is_neg()
    )

