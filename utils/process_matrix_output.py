
def process_matrix_output(poly_seq, x):
    """
    poly_seq is a polynomial remainder sequence computed either by
    (modified_)subresultants_bezout or by (modified_)subresultants_sylv.

    This function removes from poly_seq all zero polynomials as well
    as all those whose degree is equal to the degree of a preceding
    polynomial in poly_seq, as we scan it from left to right.

    """
    L = poly_seq[:]  # get a copy of the input sequence
    d = degree(L[1], x)
    i = 2
    while i < len(L):
        d_i = degree(L[i], x)
        if d_i < 0:          # zero poly
            L.remove(L[i])
            i = i - 1
        if d == d_i:         # poly degree equals degree of previous poly
            L.remove(L[i])
            i = i - 1
        if d_i >= 0:
            d = d_i
        i = i + 1

    return L

