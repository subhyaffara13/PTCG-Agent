
def sdm_matvecmul(A, B, K):
    C = {}
    for i, Ai in A.items():
        Ci = sdm_dotvec(Ai, B, K)
        if Ci:
            C[i] = Ci
    return C

