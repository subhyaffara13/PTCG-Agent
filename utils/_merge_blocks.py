
def _merge_blocks(
    blocks: list[Block], dtype: DtypeObj, can_consolidate: bool
) -> tuple[list[Block], bool]:
    if len(blocks) == 1:
        return blocks, False

    if can_consolidate:
        # TODO: optimization potential in case all mgrs contain slices and
        # combination of those slices is a slice, too.
        new_mgr_locs = np.concatenate([b.mgr_locs.as_array for b in blocks])

        new_values: ArrayLike

        if isinstance(blocks[0].dtype, np.dtype):
            # error: List comprehension has incompatible type List[Union[ndarray,
            # ExtensionArray]]; expected List[Union[complex, generic,
            # Sequence[Union[int, float, complex, str, bytes, generic]],
            # Sequence[Sequence[Any]], SupportsArray]]
            new_values = np.vstack([b.values for b in blocks])  # type: ignore[misc]
        else:
            bvals = [blk.values for blk in blocks]
            bvals2 = cast(Sequence[NDArrayBackedExtensionArray], bvals)
            new_values = bvals2[0]._concat_same_type(bvals2, axis=0)

        argsort = np.argsort(new_mgr_locs)
        new_values = new_values[argsort]
        new_mgr_locs = new_mgr_locs[argsort]

        bp = BlockPlacement(new_mgr_locs)
        return [new_block_2d(new_values, placement=bp)], True

    # can't consolidate --> no merge
    return blocks, False

