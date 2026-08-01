
def is_smith_normal_form(m, domain=None):
    '''
    Checks that the matrix is in Smith Normal Form
    '''
    dM = _to_domain(m, domain)
    return _is_snf(dM)


def is_smith_normal_form(m):
    '''
    Checks that the matrix is in Smith Normal Form
    '''
    domain = m.domain
    shape = m.shape
    zero = domain.zero
    m = m.to_list()

    for i in range(shape[0]):
        for j in range(shape[1]):
            if i == j:
                continue
            if not m[i][j] == zero:
                return False

    upper = min(shape[0], shape[1])
    for i in range(1, upper):
        if m[i-1][i-1] == zero:
            if m[i][i] != zero:
                return False
        else:
            r = domain.div(m[i][i], m[i-1][i-1])[1]
            if r != zero:
                return False

    return True

