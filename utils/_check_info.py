
def _check_info(info, driver, positive='did not converge (LAPACK info=%d)'):
    """Check info return value."""
    if info < 0:
        raise ValueError(f'illegal value in argument {-info} of internal {driver}')
    if info > 0 and positive:
        raise LinAlgError(("%s " + positive) % (driver, info,))

