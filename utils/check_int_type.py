
def check_int_type(mat):
    return np.issubdtype(mat.dtype, np.signedinteger) or np.issubdtype(
        mat.dtype, np.ulong
    )

