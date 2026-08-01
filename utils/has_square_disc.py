
def has_square_disc(T):
    """Convenience to check if a Poly or dup has square discriminant. """
    d = T.discriminant() if isinstance(T, Poly) else dup_discriminant(T, ZZ)
    return is_square(d)

