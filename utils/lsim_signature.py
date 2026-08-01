
def lsim_signature(system, U, T, X0=None, interp=True):
    return array_namespace(*_skip_if_lti(system), U, T, X0)

