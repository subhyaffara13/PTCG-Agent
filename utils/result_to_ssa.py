
def result_to_ssa(value: cute.Numeric, dtype: str) -> cute.TensorSSA:
    """
    Convert non-SSA result back to SSA form.

    After performing operations with non-SSA values (like indexed loads),
    convert the result back to SSA form for further computation.
    """
    frag = cute.make_rmem_tensor(1, dtype)
    frag[0] = value
    return frag.load()

