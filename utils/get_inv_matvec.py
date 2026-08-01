
def get_inv_matvec(M, hermitian=False, tol=0):
    if isdense(M):
        return LuInv(M).matvec
    elif issparse(M) or is_pydata_spmatrix(M):
        M = _fast_spmatrix_to_csc(M, hermitian=hermitian)
        return SpLuInv(M).matvec
    else:
        return IterInv(M, tol=tol).matvec

