
def expm_frechet_algo_64(A, E):
    n = A.shape[0]
    s = None
    ident = np.identity(n)
    A_norm_1 = scipy.linalg.norm(A, 1)
    m_pade_pairs = (
            (3, _diff_pade3),
            (5, _diff_pade5),
            (7, _diff_pade7),
            (9, _diff_pade9))
    for m, pade in m_pade_pairs:
        if A_norm_1 <= ell_table_61[m]:
            U, V, Lu, Lv = pade(A, E, ident)
            s = 0
            break
    if s is None:
        # scaling
        s = max(0, int(np.ceil(np.log2(A_norm_1 / ell_table_61[13]))))
        A = A * 2.0**-s
        E = E * 2.0**-s
        # pade order 13
        A2 = np.dot(A, A)
        M2 = np.dot(A, E) + np.dot(E, A)
        A4 = np.dot(A2, A2)
        M4 = np.dot(A2, M2) + np.dot(M2, A2)
        A6 = np.dot(A2, A4)
        M6 = np.dot(A4, M2) + np.dot(M4, A2)
        b = (64764752532480000., 32382376266240000., 7771770303897600.,
                1187353796428800., 129060195264000., 10559470521600.,
                670442572800., 33522128640., 1323241920., 40840800., 960960.,
                16380., 182., 1.)
        W1 = b[13]*A6 + b[11]*A4 + b[9]*A2
        W2 = b[7]*A6 + b[5]*A4 + b[3]*A2 + b[1]*ident
        Z1 = b[12]*A6 + b[10]*A4 + b[8]*A2
        Z2 = b[6]*A6 + b[4]*A4 + b[2]*A2 + b[0]*ident
        W = np.dot(A6, W1) + W2
        U = np.dot(A, W)
        V = np.dot(A6, Z1) + Z2
        Lw1 = b[13]*M6 + b[11]*M4 + b[9]*M2
        Lw2 = b[7]*M6 + b[5]*M4 + b[3]*M2
        Lz1 = b[12]*M6 + b[10]*M4 + b[8]*M2
        Lz2 = b[6]*M6 + b[4]*M4 + b[2]*M2
        Lw = np.dot(A6, Lw1) + np.dot(M6, W1) + Lw2
        Lu = np.dot(A, Lw) + np.dot(E, W)
        Lv = np.dot(A6, Lz1) + np.dot(M6, Z1) + Lz2
    # factor once and solve twice
    lu_piv = scipy.linalg.lu_factor(-U + V)
    R = scipy.linalg.lu_solve(lu_piv, U + V)
    L = scipy.linalg.lu_solve(lu_piv, Lu + Lv + np.dot((Lu - Lv), R))
    # squaring
    for k in range(s):
        L = np.dot(R, L) + np.dot(L, R)
        R = np.dot(R, R)
    return R, L

