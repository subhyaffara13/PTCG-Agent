
def _suffix_for(req):
    """Return the 'extras_require' suffix for a given requirement."""
    return ':' + str(req.marker) if req.marker else ''

