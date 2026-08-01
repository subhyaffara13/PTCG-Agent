
def _make_identity_transforms() -> TransFuncs:

    def identity(x):
        return x

    return identity, identity

