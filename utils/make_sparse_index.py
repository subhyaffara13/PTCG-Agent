
def make_sparse_index(length: int, indices, kind: Literal["block"]) -> BlockIndex: ...


def make_sparse_index(length: int, indices, kind: Literal["integer"]) -> IntIndex: ...


def make_sparse_index(length: int, indices, kind: SparseIndexKind) -> SparseIndex:
    index: SparseIndex
    if kind == "block":
        locs, lens = splib.get_blocks(indices)
        index = BlockIndex(length, locs, lens)
    elif kind == "integer":
        index = IntIndex(length, indices)
    else:  # pragma: no cover
        raise ValueError("must be block or integer type")
    return index

