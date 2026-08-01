
def step_signature(system, X0=None, T=None, N=None):
    return array_namespace(*_skip_if_lti(system), X0, T)

