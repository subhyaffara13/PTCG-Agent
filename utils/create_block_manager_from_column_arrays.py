
def create_block_manager_from_column_arrays(
    arrays: list[ArrayLike],
    axes: list[Index],
    consolidate: bool,
    refs: list,
) -> BlockManager:
    # Assertions disabled for performance (caller is responsible for verifying)
    # assert isinstance(axes, list)
    # assert all(isinstance(x, Index) for x in axes)
    # assert all(isinstance(x, (np.ndarray, ExtensionArray)) for x in arrays)
    # assert all(type(x) is not NumpyExtensionArray for x in arrays)
    # assert all(x.ndim == 1 for x in arrays)
    # assert all(len(x) == len(axes[1]) for x in arrays)
    # assert len(arrays) == len(axes[0])
    # These last three are sufficient to allow us to safely pass
    #  verify_integrity=False below.

    try:
        blocks = _form_blocks(arrays, consolidate, refs)
        mgr = BlockManager(blocks, axes, verify_integrity=False)
    except ValueError as e:
        raise_construction_error(len(arrays), arrays[0].shape, axes, e)
    if consolidate:
        mgr._consolidate_inplace()
    return mgr

