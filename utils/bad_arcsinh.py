
def bad_arcsinh():
    """The blocklisted trig functions are not accurate on aarch64/PPC for
    complex256. Rather than dig through the actual problem skip the
    test. This should be fixed when we can move past glibc2.17
    which is the version in manylinux2014
    """
    if platform.machine() == 'aarch64':
        x = 1.78e-10
    elif on_powerpc():
        x = 2.16e-10
    else:
        return False
    v1 = np.arcsinh(np.float128(x))
    v2 = np.arcsinh(np.complex256(x)).real
    # The eps for float128 is 1-e33, so this is way bigger
    return abs((v1 / v2) - 1.0) > 1e-23

