
def prologue_preserves_zero_mask(prologue: "SchedulerNode") -> bool:
    """
    Does this prologue preserve zero masks
    """
    preserves_zeros = PreservesZeros()
    with V.set_ops_handler(preserves_zeros):
        prologue._body(*prologue.get_ranges())

    store_preserves_zeros = preserves_zeros.store_preserves_zeros
    assert isinstance(store_preserves_zeros, bool)

    return store_preserves_zeros

