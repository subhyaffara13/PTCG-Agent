import re

def compare_or_regex_search(
    a: ArrayLike, b: Scalar | Pattern, regex: bool, mask: npt.NDArray[np.bool_]
) -> ArrayLike:
    """
    Compare two array-like inputs of the same shape or two scalar values

    Calls operator.eq or re.search, depending on regex argument. If regex is
    True, perform an element-wise regex matching.

    Parameters
    ----------
    a : array-like
    b : scalar or regex pattern
    regex : bool
    mask : np.ndarray[bool]

    Returns
    -------
    mask : array-like of bool
    """
    if isna(b):
        return ~mask

    def _check_comparison_types(
        result: ArrayLike | bool, a: ArrayLike, b: Scalar | Pattern
    ) -> None:
        """
        Raises an error if the two arrays (a,b) cannot be compared.
        Otherwise, returns the comparison result as expected.
        """
        if is_bool(result) and isinstance(a, np.ndarray):
            type_names = [type(a).__name__, type(b).__name__]

            type_names[0] = f"ndarray(dtype={a.dtype})"

            raise TypeError(
                f"Cannot compare types {type_names[0]!r} and {type_names[1]!r}"
            )

    if not regex or not should_use_regex(regex, b):
        # TODO: should use missing.mask_missing?
        op = lambda x: operator.eq(x, b)
    else:
        op = np.vectorize(
            lambda x: (
                bool(re.search(b, x))
                if isinstance(x, str) and isinstance(b, (str, Pattern))
                else False
            ),
            otypes=[bool],
        )

    # GH#32621 use mask to avoid comparing to NAs
    if isinstance(a, np.ndarray) and mask is not None:
        a = a[mask]
        result = op(a)

        if isinstance(result, np.ndarray):
            # The shape of the mask can differ to that of the result
            # since we may compare only a subset of a's or b's elements
            tmp = np.zeros(mask.shape, dtype=np.bool_)
            np.place(tmp, mask, result)
            result = tmp
    else:
        result = op(a)

    _check_comparison_types(result, a, b)
    return result

