
def l1_regression_prob(seed=0, m=8, d=9, n=100):
    '''
    Training data is {(x0, y0), (x1, y2), ..., (xn-1, yn-1)}
        x in R^d
        y in R
    n: number of training samples
    d: dimension of x, i.e. x in R^d
    phi: feature map R^d -> R^m
    m: dimension of feature space
    '''
    rng = np.random.default_rng(72847583923592458453)
    phi = rng.normal(0, 1, size=(m, d))  # random feature mapping
    w_true = rng.standard_normal(m)
    x = rng.normal(0, 1, size=(d, n))  # features
    y = w_true @ (phi @ x) + rng.normal(0, 1e-5, size=n)  # measurements

    # construct the problem
    c = np.ones(m+n)
    c[:m] = 0
    A_ub = scipy.sparse.lil_array((2*n, n+m))
    idx = 0
    for ii in range(n):
        A_ub[idx, :m] = phi @ x[:, ii]
        A_ub[idx, m+ii] = -1
        A_ub[idx+1, :m] = -1*phi @ x[:, ii]
        A_ub[idx+1, m+ii] = -1
        idx += 2
    A_ub = A_ub.tocsc()
    b_ub = np.zeros(2*n)
    b_ub[0::2] = y
    b_ub[1::2] = -y
    bnds = [(None, None)]*m + [(0, None)]*n
    return c, A_ub, b_ub, bnds

