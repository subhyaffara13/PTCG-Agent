
def reduction_acc_type(reduction_type, dtype):
    scalar_type = DTYPE_TO_CPP[DTYPE_TO_COMPUTATION_DTYPE[dtype]]
    if is_welford_reduction(reduction_type):
        return f"Welford<{scalar_type}>"
    if reduction_type in ("argmin", "argmax"):
        if dtype == torch.bool:
            scalar_type = DTYPE_TO_CPP[torch.float]
        return f"IndexValue<{scalar_type}>"
    return scalar_type

