
def _compute_numerical_gradient(fn, entry, v, norm_v, nbhd_checks_fn):
    # Computes numerical directional derivative as finite difference
    # of function `fn` at input `entry`, perturbed by vector `v`.
    if _is_sparse_compressed_tensor(entry):
        # sparse compressed tensors don't implement sub/add/copy_
        # yet. However, in non-masked semantics context entry and v
        # have the same sparse indices ...
        if entry.layout != v.layout:
            raise AssertionError(
                f"Expected entry and v to have the same layout, but got {entry.layout} and {v.layout}"
            )
        if entry._nnz() != v._nnz():
            raise AssertionError(
                f"Expected entry and v to have the same nnz, but got {entry._nnz()} and {v._nnz()} "
                f"with entry shape {entry.shape}"
            )
        # ... the finite differencing can be performed on values only:
        entry = entry.values()
        v = v.values()
        # we'll detach to avoid backward computations that sparse
        # tensors have limited support for.
        entry = entry.detach()

    orig = entry.clone()
    entry.copy_(orig - v)
    outa = fn()
    entry.copy_(orig + v)
    outb = fn()
    entry.copy_(orig)

    def compute(a, b):
        nbhd_checks_fn(a, b)
        ret = (b - a) / (2 * norm_v)  # use central difference approx
        return ret.detach().reshape(-1)

    return tuple(compute(a, b) for (a, b) in zip(outa, outb))

