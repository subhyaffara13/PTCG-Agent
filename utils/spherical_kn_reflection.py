
def spherical_kn_reflection(n, z, derivative=False):
    # More complex than the other cases, and this will likely be re-implemented
    # in C++ anyway. Would require multiple function evaluations. Probably about
    # as fast to just resort to complex math, and much simpler.
    return spherical_kn(n, z + 0j, derivative=derivative).real

