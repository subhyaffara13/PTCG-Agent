
def axlabel(xlabel, ylabel, **kwargs):
    """Grab current axis and label it.

    DEPRECATED: will be removed in a future version.

    """
    msg = "This function is deprecated and will be removed in a future version"
    warnings.warn(msg, FutureWarning)
    ax = plt.gca()
    ax.set_xlabel(xlabel, **kwargs)
    ax.set_ylabel(ylabel, **kwargs)

