
def _moment(data, n, mu=None):
    if mu is None:
        mu = data.mean()
    return ((data - mu)**n).mean()


def _moment(a, moment, axis, *, mean=None):
    if np.abs(moment - np.round(moment)) > 0:
        raise ValueError("All moment parameters must be integers")

    if moment == 0 or moment == 1:
        # By definition the zeroth moment about the mean is 1, and the first
        # moment is 0.
        shape = list(a.shape)
        del shape[axis]
        dtype = a.dtype.type if a.dtype.kind in 'fc' else np.float64

        if len(shape) == 0:
            return dtype(1.0 if moment == 0 else 0.0)
        else:
            return (ma.ones(shape, dtype=dtype) if moment == 0
                    else ma.zeros(shape, dtype=dtype))
    else:
        # Exponentiation by squares: form exponent sequence
        n_list = [moment]
        current_n = moment
        while current_n > 2:
            if current_n % 2:
                current_n = (current_n-1)/2
            else:
                current_n /= 2
            n_list.append(current_n)

        # Starting point for exponentiation by squares
        mean = a.mean(axis, keepdims=True) if mean is None else mean
        a_zero_mean = a - mean
        if n_list[-1] == 1:
            s = a_zero_mean.copy()
        else:
            s = a_zero_mean**2

        # Perform multiplications
        for n in n_list[-2::-1]:
            s = s**2
            if n % 2:
                s *= a_zero_mean
        return s.mean(axis)


def _moment(a, order, axis, *, center=None, xp=None):
    """Vectorized calculation of raw moment about specified center

    When `center` is None, the mean is computed and used as the center;
    otherwise, the provided value is used as the center.
    """
    xp = array_namespace(a) if xp is None else xp

    order = xp.asarray(order, dtype=a.dtype, device=xp_device(a))
    order_0 = order == 0
    order_1 = (order == 1) & (center is None)
    center = xp.mean(a, axis=axis, keepdims=True) if center is None else center
    a_zero_mean = _demean(a, center, axis, xp=xp)
    res = xp.mean(a_zero_mean**order, axis=axis, keepdims=True)
    if a.shape[-1] > 0 and (is_lazy_array(res)
                                or xp.any(order_0) or xp.any(order_1)):
        res = xp.where(order_0, xp.ones_like(res), res)
        res = xp.where(order_1, xp.zeros_like(res), res)

    return xp.squeeze(res, axis=axis)

