
def _clean_req(req):
    """Given a Requirement, remove environment markers and return it"""
    r = Requirement(str(req))  # create a copy before modifying
    r.marker = None
    return r

