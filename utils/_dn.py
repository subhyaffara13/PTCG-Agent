
def _dn(n, prec):
    # controller for n dependence on precision
    # n = starting digit index
    # prec = the number of total digits to compute
    n += 1  # because we subtract 1 for _series

    # assert int(math.log(n + prec)/math.log(16)) ==\
    #  ((n + prec).bit_length() - 1) // 4
    return ((n + prec).bit_length() - 1) // 4 + prec + 3

