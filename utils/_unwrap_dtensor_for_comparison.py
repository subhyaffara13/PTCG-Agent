
def _unwrap_dtensor_for_comparison(actual, expected):
    """Handle DTensor inputs for assertEqual/assert_close."""
    if not _HAS_DTENSOR:
        return actual, expected
    from torch.distributed.tensor import DTensor

    actual_dt = isinstance(actual, DTensor)
    expected_dt = isinstance(expected, DTensor)
    if actual_dt and expected_dt:
        if actual.placements != expected.placements:
            raise AssertionError(
                f"DTensor placements do not match: "
                f"{actual.placements} != {expected.placements}"
            )
        if actual.device_mesh != expected.device_mesh:
            raise AssertionError(
                f"DTensor device meshes do not match: "
                f"{actual.device_mesh} != {expected.device_mesh}"
            )
        return actual.to_local(), expected.to_local()
    elif actual_dt != expected_dt:
        raise TypeError(
            "Comparing a DTensor to a non-DTensor is ambiguous. "
            "Call .full_tensor() to compare the full logical tensor "
            "or .to_local() to compare the local shard."
        )
    return actual, expected

