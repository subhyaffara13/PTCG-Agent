
def view_element_first_byte(x):
    """Construct an array viewing the first byte of each element of `x`"""
    from numpy.lib._stride_tricks_impl import DummyArray
    interface = dict(x.__array_interface__)
    interface['typestr'] = '|b1'
    interface['descr'] = [('', '|b1')]
    return np.asarray(DummyArray(interface, x))

