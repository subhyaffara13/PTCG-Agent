
def may_unify_binary_op_mask_type(a, b):
    """
    Given two cse variables, when dtype is bool, unify them to the same mask dtype and return casted cse variable.
    """
    if a.dtype == torch.bool:
        assert b.dtype == torch.bool
        mask_dtype = torch.int32
        return unify_mask_base_type(V.kernel.compute, (a, b), mask_dtype)
    return a, b

