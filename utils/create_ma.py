
def create_ma(deg_f, deg_g, row1, row2, col_num):
    '''
    Creates a ``small'' matrix M to be triangularized.

    deg_f, deg_g are the degrees of the divident and of the
    divisor polynomials respectively, deg_g > deg_f.

    The coefficients of the divident poly are the elements
    in row2 and those of the divisor poly are the elements
    in row1.

    col_num defines the number of columns of the matrix M.

    '''
    if deg_g - deg_f >= 1:
        print('Reverse degrees')
        return

    m = zeros(deg_f - deg_g + 2, col_num)

    for i in range(deg_f - deg_g + 1):
        m[i, :] = rotate_r(row1, i)
    m[deg_f - deg_g + 1, :] = row2

    return m

