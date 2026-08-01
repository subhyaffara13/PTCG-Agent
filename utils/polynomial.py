
def polynomial(order):
    """
    Factory function for a general polynomial model.

    .. deprecated:: 1.17.0
        `scipy.odr` is deprecated and will be removed in SciPy 1.19.0. Please use
        `pypi.org/project/odrpack/ <https://pypi.org/project/odrpack/>`_
        instead.

    Parameters
    ----------
    order : int or sequence
        If an integer, it becomes the order of the polynomial to fit. If
        a sequence of numbers, then these are the explicit powers in the
        polynomial.
        A constant term (power 0) is always included, so don't include 0.
        Thus, polynomial(n) is equivalent to polynomial(range(1, n+1)).

    Returns
    -------
    polynomial : Model instance
        Model instance.

    Examples
    --------
    We can fit an input data using orthogonal distance regression (ODR) with
    a polynomial model:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import odr
    >>> x = np.linspace(0.0, 5.0)
    >>> y = np.sin(x)
    >>> poly_model = odr.polynomial(3)  # using third order polynomial model
    >>> data = odr.Data(x, y)
    >>> odr_obj = odr.ODR(data, poly_model)
    >>> output = odr_obj.run()  # running ODR fitting
    >>> poly = np.poly1d(output.beta[::-1])
    >>> poly_y = poly(x)
    >>> plt.plot(x, y, label="input data")
    >>> plt.plot(x, poly_y, label="polynomial ODR")
    >>> plt.legend()
    >>> plt.show()

    """

    powers = np.asarray(order)
    if powers.shape == ():
        # Scalar.
        powers = np.arange(1, powers + 1)

    powers = powers.reshape((len(powers), 1))
    len_beta = len(powers) + 1

    def _poly_est(data, len_beta=len_beta):
        # Eh. Ignore data and return all ones.
        return np.ones((len_beta,), float)

    return Model(_poly_fcn, fjacd=_poly_fjacd, fjacb=_poly_fjacb,
                 estimate=_poly_est, extra_args=(powers,),
                 meta={'name': 'Sorta-general Polynomial',
                 'equ': 'y = B_0 + Sum[i=1..%s, B_i * (x**i)]' % (len_beta-1),
                 'TeXequ': r'$y=\beta_0 + \sum_{i=1}^{%s} \beta_i x^i$' %
                        (len_beta-1)})

