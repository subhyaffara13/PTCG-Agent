
def dlsim_signature(system, u, t=None, x0=None):
    return array_namespace(*_skip_if_lti(system), u, t, x0)

