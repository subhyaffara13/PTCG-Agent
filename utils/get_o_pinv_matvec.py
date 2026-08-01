
def get_OPinv_matvec(A, M, sigma, hermitian=False, tol=0):
    if sigma == 0:
        return get_inv_matvec(A, hermitian=hermitian, tol=tol)

    if M is None:
        #M is the identity matrix
        if isdense(A):
            if (np.issubdtype(A.dtype, np.complexfloating)
                    or np.imag(sigma) == 0):
                A = np.copy(A)
            else:
                A = A + 0j
            A.flat[::A.shape[1] + 1] -= sigma
            return LuInv(A).matvec
        elif issparse(A) or is_pydata_spmatrix(A):
            A = A - sigma * eye_array(A.shape[0])
            A = _fast_spmatrix_to_csc(A, hermitian=hermitian)
            return SpLuInv(A).matvec
        else:
            return IterOpInv(aslinearoperator(A),
                             M, sigma, tol=tol).matvec
    else:
        if ((not isdense(A) and not issparse(A) and not is_pydata_spmatrix(A)) or
                (not isdense(M) and not issparse(M) and not is_pydata_spmatrix(M))):
            return IterOpInv(aslinearoperator(A),
                             aslinearoperator(M),
                             sigma, tol=tol).matvec
        elif isdense(A) or isdense(M):
            return LuInv(A - sigma * M).matvec
        else:
            OP = A - sigma * M
            OP = _fast_spmatrix_to_csc(OP, hermitian=hermitian)
            return SpLuInv(OP).matvec

