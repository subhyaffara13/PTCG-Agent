
def ssa_to_indexable(ssa_value: cute.TensorSSA, dtype: str) -> cute.Numeric:
    """
    Convert SSA form to indexable non-SSA form.

    Workaround for lack of gather support: SSA values cannot be used directly
    as indices in tensor loads. This converts SSA → fragment → scalar for indexing.
    """
    frag = cute.make_rmem_tensor(1, dtype)
    frag.store(ssa_value)
    return frag[0]

