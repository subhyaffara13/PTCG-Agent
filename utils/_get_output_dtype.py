
def _get_output_dtype(covariance, points):
    """
    Calculates the output dtype and the "spec" (=C type name).

    This was necessary in order to deal with the fused types in the Cython
    routine `gaussian_kernel_estimate`. See gh-10824 for details.
    """
    output_dtype = np.common_type(covariance, points)
    itemsize = np.dtype(output_dtype).itemsize
    if itemsize == 4:
        spec = 'float'
    elif itemsize == 8:
        spec = 'double'
    elif itemsize in (12, 16):
        spec = 'long double'
    else:
        raise ValueError(
                f"{output_dtype} has unexpected item size: {itemsize}"
            )

    return output_dtype, spec

