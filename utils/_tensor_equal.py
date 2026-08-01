
def _tensor_equal(a1, a2, equal_nan=False):
    # Implementation of array_equal/array_equiv.
    if a1.shape != a2.shape:
        return False
    cond = a1 == a2
    if equal_nan:
        cond = cond | (torch.isnan(a1) & torch.isnan(a2))
    return cond.all().item()

