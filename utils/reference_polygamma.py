
def reference_polygamma(x, n):
    # WEIRD `scipy.special.polygamma` behavior
    # >>> scipy.special.polygamma(0, np.array(501, dtype=np.float32)).dtype
    # dtype('float64')
    # >>> scipy.special.polygamma(0, np.array([501], dtype=np.float32)).dtype
    # dtype('float32')
    #
    # Thus we cast output to the default torch dtype or preserve double
    result_dtype = torch_to_numpy_dtype_dict[torch.get_default_dtype()]
    if x.dtype == np.double:
        result_dtype = np.double
    return scipy.special.polygamma(n, x).astype(result_dtype)

