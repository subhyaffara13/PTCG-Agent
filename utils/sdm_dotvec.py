
def sdm_dotvec(A, B, K):
    return K.sum(A[j] * B[j] for j in A.keys() & B.keys())

