
def freqresp_signature(system, w=None, n=10000):
    return array_namespace(*_skip_if_lti(system), w)

