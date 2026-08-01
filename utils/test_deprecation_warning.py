
def test_deprecation_warning():
    w = SymPyDeprecationWarning("message", deprecated_since_version='1.0', active_deprecations_target="active-deprecations")
    check(w)

