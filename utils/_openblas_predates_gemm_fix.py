
def _openblas_predates_gemm_fix(name, version):
    if 'openblas' not in name:
        return False
    try:
        parsed = tuple(int(p) for p in version.split('.'))
    except ValueError:
        return False
    return parsed < (0, 3, 33, 112)

