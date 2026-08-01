
def make_tensor_mismatch_msg(
    actual: torch.Tensor,
    expected: torch.Tensor,
    matches: torch.Tensor,
    *,
    rtol: float,
    atol: float,
    identifier: str | Callable[[str], str] | None = None,
):
    """Makes a mismatch error message for tensors.

    Args:
        actual (torch.Tensor): Actual tensor.
        expected (torch.Tensor): Expected tensor.
        matches (torch.Tensor): Boolean mask of the same shape as ``actual`` and ``expected`` that indicates the
            location of matches.
        rtol (float): Relative tolerance.
        atol (float): Absolute tolerance.
        identifier (Optional[Union[str, Callable[[str], str]]]): Optional description for the tensors. Can be passed
            as callable in which case it will be called by the default value to create the description at runtime.
            Defaults to "Tensor-likes".
    """

    def unravel_flat_index(flat_index: int) -> tuple[int, ...]:
        if not matches.shape:
            return ()

        inverse_index = []
        for size in matches.shape[::-1]:
            div, mod = divmod(flat_index, size)
            flat_index = div
            inverse_index.append(mod)

        return tuple(inverse_index[::-1])

    number_of_elements = matches.numel()
    total_mismatches = number_of_elements - int(torch.sum(matches))
    extra = (
        f"Mismatched elements: {total_mismatches} / {number_of_elements} "
        f"({total_mismatches / number_of_elements:.1%})"
    )
    if actual.dtype.is_floating_point and actual.dtype.itemsize == 1:
        # skip checking for max_abs_diff and max_rel_diff for float8-like values
        first_mismatch_idx = tuple(torch.nonzero(~matches, as_tuple=False)[0].tolist())
        return _make_bitwise_mismatch_msg(
            default_identifier="Tensor-likes",
            identifier=identifier,
            extra=extra,
            first_mismatch_idx=first_mismatch_idx,
        )

    actual_flat = actual.flatten()
    expected_flat = expected.flatten()
    matches_flat = matches.flatten()

    if not actual.dtype.is_floating_point and not actual.dtype.is_complex:
        # TODO: Instead of always upcasting to int64, it would be sufficient to cast to the next higher dtype to avoid
        #  overflow
        actual_flat = actual_flat.to(torch.int64)
        expected_flat = expected_flat.to(torch.int64)

    abs_diff = torch.abs(actual_flat - expected_flat)
    # Ensure that only mismatches are used for the max_abs_diff computation
    abs_diff[matches_flat] = 0
    max_abs_diff, max_abs_diff_flat_idx = torch.max(abs_diff, 0)

    rel_diff = abs_diff / torch.abs(expected_flat)
    # Ensure that only mismatches are used for the max_rel_diff computation
    rel_diff[matches_flat] = 0
    max_rel_diff, max_rel_diff_flat_idx = torch.max(rel_diff, 0)
    return _make_mismatch_msg(
        default_identifier="Tensor-likes",
        identifier=identifier,
        extra=extra,
        abs_diff=max_abs_diff.item(),
        abs_diff_idx=unravel_flat_index(int(max_abs_diff_flat_idx)),
        atol=atol,
        rel_diff=max_rel_diff.item(),
        rel_diff_idx=unravel_flat_index(int(max_rel_diff_flat_idx)),
        rtol=rtol,
    )

