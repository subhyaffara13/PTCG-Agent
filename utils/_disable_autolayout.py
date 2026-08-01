
def _disable_autolayout():
    """Context manager for preventing rc-controlled auto-layout behavior."""
    # This is a workaround for an issue in matplotlib, for details see
    # https://github.com/mwaskom/seaborn/issues/2914
    # The only affect of this rcParam is to set the default value for
    # layout= in plt.figure, so we could just do that instead.
    # But then we would need to own the complexity of the transition
    # from tight_layout=True -> layout="tight". This seems easier,
    # but can be removed when (if) that is simpler on the matplotlib side,
    # or if the layout algorithms are improved to handle figure legends.
    orig_val = mpl.rcParams["figure.autolayout"]
    try:
        mpl.rcParams["figure.autolayout"] = False
        yield
    finally:
        mpl.rcParams["figure.autolayout"] = orig_val

