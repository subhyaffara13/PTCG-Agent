
def median_default(self):
    if not config.triton.decompose_sort_ops:
        return median_fallback(self)
    size = self.get_size()
    numel = functools.reduce(operator.mul, size, sympy.Integer(1))
    flat = view(self, [numel])
    sorted_vals, _ = sort_stable(flat, dim=0)
    k = (numel - 1) // 2
    return select(sorted_vals, 0, k)

