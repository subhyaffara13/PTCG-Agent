
def skipCUDAIfNoMagmaAndNoCusolver(fn):
    if has_cusolver():
        return fn
    else:
        # cuSolver is disabled on cuda < 10.1.243, tests depend on MAGMA
        return skipCUDAIfNoMagma(fn)

