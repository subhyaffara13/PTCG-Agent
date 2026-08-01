
def A():
    return np.array([[0, 1, 2], [0, 0, 0], [0, 0, 0]])


def A():
    A = csr_array([[0, 1, 2], [2, 1, 0], [0, 1, 0]])
    A.indptr = A.indptr.astype(np.int64)
    A.indices = A.indices.astype(np.int64)
    return A


def A(request):
    # construct Hilbert matrix
    # set parameters
    n = 300
    yield hilbert(n).astype(request.param)


def a(df):
    return pd.concat([df, df])

