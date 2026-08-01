
def sign_seq(poly_seq, x):
    """
    Given a sequence of polynomials poly_seq, it returns
    the sequence of signs of the leading coefficients of
    the polynomials in poly_seq.

    """
    return [sign(LC(poly_seq[i], x)) for i in range(len(poly_seq))]

