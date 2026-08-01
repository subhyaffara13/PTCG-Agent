
def _tuples_to_blocks_no_consolidate(tuples, refs) -> list[Block]:
    # tuples produced within _form_blocks are of the form (placement, array)
    return [
        new_block_2d(
            ensure_block_shape(arr, ndim=2), placement=BlockPlacement(i), refs=ref
        )
        for ((i, arr), ref) in zip(tuples, refs, strict=True)
    ]

