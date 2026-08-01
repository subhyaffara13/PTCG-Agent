
def _linearoperator(mv, shape, dtype):
    return LinearOperator(matvec=mv, matmat=mv, shape=shape, dtype=dtype)

