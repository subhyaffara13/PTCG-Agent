
def _nearest_real_complex_idx(fro, to, which):
    """Get the next closest real or complex element based on distance"""
    assert which in ('real', 'complex', 'any')
    order = np.argsort(np.abs(fro - to))
    if which == 'any':
        return order[0]
    else:
        mask = np.isreal(fro[order])
        if which == 'complex':
            mask = ~mask
        return order[np.nonzero(mask)[0][0]]

