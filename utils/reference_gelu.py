
def reference_gelu(X, *, approximate='none'):
    def _gelu_ref(X):
        return X * stats.norm.cdf(X)

    def _tanh_gelu_ref(X):
        M_SQRT_2_PI = math.sqrt(2 / math.pi)
        Z = M_SQRT_2_PI * (X + 0.044715 * np.power(X, 3.0))
        return 0.5 * X * (1.0 + np.tanh(Z))

    if approximate == 'tanh':
        return _tanh_gelu_ref(X)
    else:
        return _gelu_ref(X)

