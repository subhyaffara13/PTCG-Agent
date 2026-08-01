
def estimated_warns():
    """If trace is estimated, it should warn.

    We warn that estimation of trace might impact performance.
    All result have to be correct nevertheless!
    """
    return pytest.warns(UserWarning, match="Trace of LinearOperator not available")

