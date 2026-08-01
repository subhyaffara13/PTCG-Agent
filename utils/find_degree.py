
def find_degree(M, deg_f):
    '''
    Finds the degree of the poly corresponding (after triangularization)
    to the _last_ row of the ``small'' matrix M, created by create_ma().

    deg_f is the degree of the divident poly.
    If _last_ row is all 0's returns None.

    '''
    j = deg_f
    for i in range(0, M.cols):
        if M[M.rows - 1, i] == 0:
            j = j - 1
        else:
            return max(j, 0)

