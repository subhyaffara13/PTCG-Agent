import itertools

def generate_indices(f, values=False):
    """
    generate the indices
    if values is True , use the axis values
    is False, use the range
    """
    axes = f.axes
    if values:
        axes = (list(range(len(ax))) for ax in axes)

    return itertools.product(*axes)

