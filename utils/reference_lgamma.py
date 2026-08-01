
def reference_lgamma(x):
    # scipy.special.gammaln returns `-inf` when input is `-inf`.
    # While Pytorch, C and C++, all return `inf` when input is `-inf`.
    # Reference:
    # https://en.cppreference.com/w/cpp/numeric/math/lgamma
    # https://en.cppreference.com/w/c/numeric/math/lgamma

    # To handle the above discrepancy,
    # we replace -inf with inf so values
    # that were originally -inf map to inf as expected
    if x.dtype.kind == 'f':
        x = np.where(x == float('-inf'), np.array(float('inf'), dtype=x.dtype), x)

    out = scipy.special.gammaln(x)

    if x.dtype == np.float16:
        # `scipy.special.gammaln` returns output of float32 when input is float16,
        # while `torch.lgamma` preserves `float16`. But due to smaller range of float16,
        # Pytorch version outputs `inf` while SciPy returns finite values.
        out = out.astype(np.float16)

    return out

