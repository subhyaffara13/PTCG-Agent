
def _exp_sinch(a, x):
    """
    Stably evaluate exp(a)*sinh(x)/x

    Notes
    -----
    The strategy of falling back to a sixth order Taylor expansion
    was suggested by the Spallation Neutron Source docs
    which was found on the internet by google search.
    http://www.ornl.gov/~t6p/resources/xal/javadoc/gov/sns/tools/math/ElementaryFunction.html
    The details of the cutoff point and the Horner-like evaluation
    was picked without reference to anything in particular.

    Note that sinch is not currently implemented in scipy.special,
    whereas the "engineer's" definition of sinc is implemented.
    The implementation of sinc involves a scaling factor of pi
    that distinguishes it from the "mathematician's" version of sinc.

    """

    # If x is small then use sixth order Taylor expansion.
    # How small is small? I am using the point where the relative error
    # of the approximation is less than 1e-14.
    # If x is large then directly evaluate sinh(x) / x.
    if abs(x) < 0.0135:
        x2 = x*x
        return np.exp(a) * (1 + (x2/6.)*(1 + (x2/20.)*(1 + (x2/42.))))
    else:
        return (np.exp(a + x) - np.exp(a - x)) / (2*x)

