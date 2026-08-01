
def is_float_or_fp_tensor(x):
    return _dtype_for_scalar_or_tensor(x).is_floating_point

