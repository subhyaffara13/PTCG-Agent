
def _get_same_shape_values(
    lblk: Block, rblk: Block, left_ea: bool, right_ea: bool
) -> tuple[ArrayLike, ArrayLike]:
    """
    Slice lblk.values to align with rblk.  Squeeze if we have EAs.
    """
    lvals = lblk.values
    rvals = rblk.values

    # Require that the indexing into lvals be slice-like
    assert rblk.mgr_locs.is_slice_like, rblk.mgr_locs

    # TODO(EA2D): with 2D EAs only this first clause would be needed
    if not (left_ea or right_ea):
        # error: No overload variant of "__getitem__" of "ExtensionArray" matches
        # argument type "Tuple[Union[ndarray, slice], slice]"
        lvals = lvals[rblk.mgr_locs.indexer, :]  # type: ignore[call-overload]
        assert lvals.shape == rvals.shape, (lvals.shape, rvals.shape)
    elif left_ea and right_ea:
        assert lvals.shape == rvals.shape, (lvals.shape, rvals.shape)
    elif right_ea:
        # lvals are 2D, rvals are 1D

        # error: No overload variant of "__getitem__" of "ExtensionArray" matches
        # argument type "Tuple[Union[ndarray, slice], slice]"
        lvals = lvals[rblk.mgr_locs.indexer, :]  # type: ignore[call-overload]
        assert lvals.shape[0] == 1, lvals.shape
        lvals = lvals[0, :]
    else:
        # lvals are 1D, rvals are 2D
        assert rvals.shape[0] == 1, rvals.shape
        # error: No overload variant of "__getitem__" of "ExtensionArray" matches
        # argument type "Tuple[int, slice]"
        rvals = rvals[0, :]  # type: ignore[call-overload]

    return lvals, rvals

