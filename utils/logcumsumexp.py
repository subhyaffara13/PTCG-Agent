
def logcumsumexp(self, dim):
    # Checks that dim is within bounds
    maybe_wrap_dim(dim, self.ndim)
    return torch.empty_like(self, memory_format=torch.contiguous_format)


def logcumsumexp(x, dim):
    def log_add_exp_helper(a_tuple, b_tuple):
        (a,) = a_tuple
        (b,) = b_tuple
        min_v = ops.minimum(a, b)
        max_v = ops.maximum(a, b)
        mask = (min_v != max_v) | (~ops.isinf(min_v))
        return (ops.where(mask, ops.log1p(ops.exp(min_v - max_v)) + max_v, a),)

    dtype = x.get_dtype()
    if len(x.get_size()) == 0:
        assert dim in [0, -1]
        return clone(x)

    kwargs = _make_scan_inner(x, axis=dim, dtype=dtype)
    (result,) = ir.Scan.create(**kwargs, combine_fn=log_add_exp_helper)
    if result is None:
        return fallback_logcumsumexp(x, dim=dim)
    return result

