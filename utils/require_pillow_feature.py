
def require_pillow_feature(name):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        available = features.check(name.lower())
    return pytest.mark.skipif(not available, reason=f"{name} support not available")

