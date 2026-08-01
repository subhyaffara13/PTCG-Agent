
def dimpulse_signature(system, x0=None, t=None, n=None):
    return array_namespace(*_skip_if_lti(system), x0, t)

