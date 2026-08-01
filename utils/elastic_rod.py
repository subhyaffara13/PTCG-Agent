
def ElasticRod(n):
    """Build the matrices for the generalized eigenvalue problem of the
    fixed-free elastic rod vibration model.
    """
    L = 1.0
    le = L/n
    rho = 7.85e3
    S = 1.e-4
    E = 2.1e11
    mass = rho*S*le/6.
    k = E*S/le
    A = k*(diag(r_[2.*ones(n-1), 1])-diag(ones(n-1), 1)-diag(ones(n-1), -1))
    B = mass*(diag(r_[4.*ones(n-1), 2])+diag(ones(n-1), 1)+diag(ones(n-1), -1))
    return A, B

