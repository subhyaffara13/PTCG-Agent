
def _diff_pade3(A, E, ident):
    b = (120., 60., 12., 1.)
    A2 = A.dot(A)
    M2 = np.dot(A, E) + np.dot(E, A)
    U = A.dot(b[3]*A2 + b[1]*ident)
    V = b[2]*A2 + b[0]*ident
    Lu = A.dot(b[3]*M2) + E.dot(b[3]*A2 + b[1]*ident)
    Lv = b[2]*M2
    return U, V, Lu, Lv

