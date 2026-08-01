
def use_reflection(sign_n_even=None, reflection_fun=None):
    # - If reflection_fun is not specified, reflects negative `z` and multiplies
    #   output by appropriate sign (indicated by `sign_n_even`).
    # - If reflection_fun is specified, calls `reflection_fun` instead of `fun`.
    # See DLMF 10.47(v) https://dlmf.nist.gov/10.47
    def decorator(fun):
        def standard_reflection(n, z, derivative):
            # sign_n_even indicates the sign when the order `n` is even
            sign = np.where(n % 2 == 0, sign_n_even, -sign_n_even)
            # By the chain rule, differentiation at `-z` adds a minus sign
            sign = -sign if derivative else sign
            # Evaluate at positive z (minus negative z) and adjust the sign
            return fun(n, -z, derivative) * sign

        @wraps(fun)
        def wrapper(n, z, derivative=False):
            z = np.asarray(z)

            if np.issubdtype(z.dtype, np.complexfloating):
                return fun(n, z, derivative)  # complex dtype just works

            f2 = standard_reflection if reflection_fun is None else reflection_fun
            return xpx.apply_where(z.real >= 0, (n, z),
                                   lambda n, z: fun(n, z, derivative),
                                   lambda n, z: f2(n, z, derivative))[()]
        return wrapper
    return decorator

