
def _warn_jac_unused(jac, method):
    if jac is not None:
        warn(f'Method {method} does not use the jacobian (jac).',
             RuntimeWarning, stacklevel=2)

