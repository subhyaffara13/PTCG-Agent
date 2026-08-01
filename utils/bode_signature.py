
def bode_signature(system, w=None, n=100):
    return array_namespace(*_skip_if_lti(system), w)

