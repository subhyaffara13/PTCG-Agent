
def _is_non_overlapping_and_dense_or_false(sizes, strides) -> bool:
    """
    Helper function for is_non_overlapping_and_dense.
    For unbacked sizes & strides, returns True only if symbolically non-overlapping & dense,
    and False otherwise.

    e.g. sizes: [u0, u1], strides: [u2, u3]
    this may be non-overlapping & dense at runtime, for values {u0: 4, u1: 4, u2: 4, u3: 1},
    but isn't true for all values.
    """
    from torch.fx.experimental.symbolic_shapes import guard_or_false, guard_or_true
    from torch.utils._sympy.functions import Max

    # Short-circuits for 0/1-element tensors
    if guard_or_false(prod(sizes) < 2):  # type: ignore[operator]
        return True

    # Short-circuits for tensors of rank one, which are
    # non-overlapping and "dense" if their stride is one
    if len(sizes) == 1:
        return guard_or_false(strides[0] == 1)

    # Checks that there exists a permutation of the strides s.t. the tensor would be contiguous
    # Sorts (length, stride) pairs by stride
    #
    # This sort is done in a size-oblivious way, which helps if we do a
    # comparison like 2048*u0 > u0; we just want this to return True
    # (and not worry about what if u0 is zero).
    class K(NamedTuple):
        size: int
        stride: int

        def __lt__(self, other):
            # for backed symbols, this is practically a < operation
            # for unbacked, we return True if < is statically known,
            # then try to answer this symbolically, with stride ordering semantics
            # (e.g. u0 < u0 is False, u0 < u1 is False with no axioms, u0 < 2 * u0 is True)
            return (
                guard_or_false(
                    self.stride < other.stride
                )  # checks statically known inequality
                or (
                    (
                        guard_or_false(self.stride == 0)
                        or guard_or_false(other.stride % self.stride == 0)
                    )
                    and guard_or_true(self.stride != other.stride)
                )  # checks symbolic inequality (e.g. u0 < 2048 * u0)
            )

    lengths_and_strides = sorted(map(K, sizes, strides))

    # verify actual strides match the expected (composed sizes)
    sizes = [x.size for x in lengths_and_strides][::-1]
    strides = [x.stride for x in lengths_and_strides][::-1]
    return check_contiguous_sizes_strides(sizes, strides, false_if_dde=True)

