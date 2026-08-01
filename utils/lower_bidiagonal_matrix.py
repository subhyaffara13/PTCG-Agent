
def lowerBidiagonalMatrix(m, n):
    # This is a simple example for testing LSMR.
    # It uses the leading m*n submatrix from
    # A = [ 1
    #       1 2
    #         2 3
    #           3 4
    #             ...
    #               n ]
    # suitably padded by zeros.
    #
    # 04 Jun 2010: First version for distribution with lsmr.py
    if m <= n:
        row = hstack((arange(m, dtype=int),
                      arange(1, m, dtype=int)))
        col = hstack((arange(m, dtype=int),
                      arange(m-1, dtype=int)))
        data = hstack((arange(1, m+1, dtype=float),
                       arange(1,m, dtype=float)))
        return coo_array((data, (row, col)), shape=(m,n))
    else:
        row = hstack((arange(n, dtype=int),
                      arange(1, n+1, dtype=int)))
        col = hstack((arange(n, dtype=int),
                      arange(n, dtype=int)))
        data = hstack((arange(1, n+1, dtype=float),
                       arange(1,n+1, dtype=float)))
        return coo_array((data,(row, col)), shape=(m,n))

