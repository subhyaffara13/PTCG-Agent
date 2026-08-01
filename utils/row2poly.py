
def row2poly(row, deg, x):
    '''
    Converts the row of a matrix to a poly of degree deg and variable x.
    Some entries at the beginning and/or at the end of the row may be zero.

    '''
    k = 0
    poly = []
    leng = len(row)

    # find the beginning of the poly ; i.e. the first
    # non-zero element of the row
    while row[k] == 0:
        k = k + 1

    # append the next deg + 1 elements to poly
    for j in range( deg + 1):
        if k + j <= leng:
            poly.append(row[k + j])

    return Poly(poly, x)

