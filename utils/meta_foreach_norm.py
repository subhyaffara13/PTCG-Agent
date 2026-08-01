
def meta_foreach_norm(tensors, ord=2, dtype=None):
    if float(ord) == float("inf"):
        for t in tensors:
            torch._check(
                t.numel() > 0,
                lambda: "_foreach_norm cannot compute infinity norm on empty tensor",
            )
    results = []
    for t in tensors:
        out_dtype = dtype if dtype is not None else t.dtype
        if out_dtype.is_complex:
            out_dtype = corresponding_real_dtype(out_dtype)
        results.append(t.new_empty((), dtype=out_dtype))
    return results

