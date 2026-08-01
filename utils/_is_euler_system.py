
def _is_euler_system(As, t):
    return all(_matrix_is_constant((A*t**i).applyfunc(ratsimp), t) for i, A in enumerate(As))

