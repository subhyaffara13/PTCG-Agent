
def bmm_einsum(eq, a, b, out=None, **kwargs):
    """Perform arbitrary pairwise einsums using only ``matmul``, or
    ``multiply`` if no contracted indices are involved (plus maybe single term
    ``einsum`` to prepare the terms individually). The logic for each is cached
    based on the equation and array shape, and each step is only performed if
    necessary.

    Parameters
    ----------
    eq : str
        The einsum equation.
    a : array_like
        The first array to contract.
    b : array_like
        The second array to contract.

    Returns
    -------
    array_like

    Notes
    -----
    A fuller description of this algorithm, and original source for this
    implementation, can be found at https://github.com/jcmgray/einsum_bmm.
    """
    (
        eq_a,
        eq_b,
        new_shape_a,
        new_shape_b,
        new_shape_ab,
        perm_ab,
        pure_multiplication,
    ) = _parse_eq_to_batch_matmul(eq, a.shape, b.shape)

    # n.b. one could special case various cases to call c_einsum directly here

    # need to handle `order` a little manually, since we do transpose
    # operations before and potentially after the ufunc calls
    output_order = _parse_output_order(
        kwargs.pop("order", "K"), a.flags.f_contiguous, b.flags.f_contiguous
    )

    # prepare left
    if eq_a is not None:
        # diagonals, sums, and transpose
        a = c_einsum(eq_a, a)
    if new_shape_a is not None:
        a = reshape(a, new_shape_a)

    # prepare right
    if eq_b is not None:
        # diagonals, sums, and transpose
        b = c_einsum(eq_b, b)
    if new_shape_b is not None:
        b = reshape(b, new_shape_b)

    if pure_multiplication:
        # no contracted indices
        if output_order is not None:
            kwargs["order"] = output_order

        # do the 'contraction' via multiplication!
        return multiply(a, b, out=out, **kwargs)

    # can only supply out here if no other reshaping / transposing
    matmul_out_compatible = (new_shape_ab is None) and (perm_ab is None)
    if matmul_out_compatible:
        kwargs["out"] = out

    # do the contraction!
    ab = matmul(a, b, **kwargs)

    # prepare the output
    if new_shape_ab is not None:
        ab = reshape(ab, new_shape_ab)
    if perm_ab is not None:
        ab = ab.transpose(perm_ab)

    if (out is not None) and (not matmul_out_compatible):
        # handle case where out is specified, but we also needed
        # to reshape / transpose ``ab`` after the matmul
        out[...] = ab
        ab = out
    elif output_order is not None:
        ab = asanyarray(ab, order=output_order)

    return ab

