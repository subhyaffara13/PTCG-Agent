
def _parse_eq_to_batch_matmul(eq, shape_a, shape_b):
    """Cached parsing of a two term einsum equation into the necessary
    sequence of arguments for contraction via batched matrix multiplication.
    The steps we need to specify are:

        1. Remove repeated and trivial indices from the left and right terms,
           and transpose them, done as a single einsum.
        2. Fuse the remaining indices so we have two 3D tensors.
        3. Perform the batched matrix multiplication.
        4. Unfuse the output to get the desired final index order.

    """
    lhs, out = eq.split("->")
    a_term, b_term = lhs.split(",")

    if len(a_term) != len(shape_a):
        raise ValueError(f"Term '{a_term}' does not match shape {shape_a}.")
    if len(b_term) != len(shape_b):
        raise ValueError(f"Term '{b_term}' does not match shape {shape_b}.")

    sizes = {}
    singletons = set()

    # parse left term to unique indices with size > 1
    left = {}
    for ix, d in zip(a_term, shape_a):
        if d == 1:
            # everything (including broadcasting) works nicely if simply ignore
            # such dimensions, but we do need to track if they appear in output
            # and thus should be reintroduced later
            singletons.add(ix)
            continue
        if sizes.setdefault(ix, d) != d:
            # set and check size
            raise ValueError(
                f"Index {ix} has mismatched sizes {sizes[ix]} and {d}."
            )
        left[ix] = True

    # parse right term to unique indices with size > 1
    right = {}
    for ix, d in zip(b_term, shape_b):
        # broadcast indices (size 1 on one input and size != 1
        # on the other) should not be treated as singletons
        if d == 1:
            if ix not in left:
                singletons.add(ix)
            continue
        singletons.discard(ix)

        if sizes.setdefault(ix, d) != d:
            # set and check size
            raise ValueError(
                f"Index {ix} has mismatched sizes {sizes[ix]} and {d}."
            )
        right[ix] = True

    # now we classify the unique size > 1 indices only
    bat_inds = []  # appears on A, B, O
    con_inds = []  # appears on A, B, .
    a_keep = []  # appears on A, ., O
    b_keep = []  # appears on ., B, O
    # other indices (appearing on A or B only) will
    # be summed or traced out prior to the matmul
    for ix in left:
        if right.pop(ix, False):
            if ix in out:
                bat_inds.append(ix)
            else:
                con_inds.append(ix)
        elif ix in out:
            a_keep.append(ix)
    # now only indices unique to right remain
    for ix in right:
        if ix in out:
            b_keep.append(ix)

    if not con_inds:
        # contraction is pure multiplication, prepare inputs differently
        return _parse_eq_to_pure_multiplication(
            a_term, shape_a, b_term, shape_b, out
        )

    # only need the size one indices that appear in the output
    singletons = [ix for ix in out if ix in singletons]

    # take diagonal, remove any trivial axes and transpose left
    desired_a = "".join((*bat_inds, *a_keep, *con_inds))
    if a_term != desired_a:
        eq_a = f"{a_term}->{desired_a}"
    else:
        eq_a = None

    # take diagonal, remove any trivial axes and transpose right
    desired_b = "".join((*bat_inds, *con_inds, *b_keep))
    if b_term != desired_b:
        eq_b = f"{b_term}->{desired_b}"
    else:
        eq_b = None

    # then we want to reshape
    if bat_inds:
        lgroups = (bat_inds, a_keep, con_inds)
        rgroups = (bat_inds, con_inds, b_keep)
        ogroups = (bat_inds, a_keep, b_keep)
    else:
        # avoid size 1 batch dimension if no batch indices
        lgroups = (a_keep, con_inds)
        rgroups = (con_inds, b_keep)
        ogroups = (a_keep, b_keep)

    if any(len(group) != 1 for group in lgroups):
        # need to fuse 'kept' and contracted indices
        # (though could allow batch indices to be broadcast)
        new_shape_a = tuple(
            functools.reduce(operator.mul, (sizes[ix] for ix in ix_group), 1)
            for ix_group in lgroups
        )
    else:
        new_shape_a = None

    if any(len(group) != 1 for group in rgroups):
        # need to fuse 'kept' and contracted indices
        # (though could allow batch indices to be broadcast)
        new_shape_b = tuple(
            functools.reduce(operator.mul, (sizes[ix] for ix in ix_group), 1)
            for ix_group in rgroups
        )
    else:
        new_shape_b = None

    if any(len(group) != 1 for group in ogroups) or singletons:
        new_shape_ab = (1,) * len(singletons) + tuple(
            sizes[ix] for ix_group in ogroups for ix in ix_group
        )
    else:
        new_shape_ab = None

    # then we might need to permute the matmul produced output:
    out_produced = "".join((*singletons, *bat_inds, *a_keep, *b_keep))
    if out_produced != out:
        perm_ab = tuple(out_produced.index(ix) for ix in out)
    else:
        perm_ab = None

    return (
        eq_a,
        eq_b,
        new_shape_a,
        new_shape_b,
        new_shape_ab,
        perm_ab,
        False,  # pure_multiplication=False
    )

