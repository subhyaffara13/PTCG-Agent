
def check_private_entropy(distfn, args, superclass):
    # compare a generic _entropy with the distribution-specific implementation
    npt.assert_allclose(distfn._entropy(*args),
                        superclass._entropy(distfn, *args))

