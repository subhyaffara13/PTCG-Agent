
def _DM(lol, typ, K):
    """Make a DM of type typ over K from lol."""
    A = DM(lol, K)

    if typ == 'DDM':
        return A.to_ddm()
    elif typ == 'SDM':
        return A.to_sdm()
    elif typ == 'DFM':
        if GROUND_TYPES != 'flint':
            skip("DFM not supported in this ground type")
        return A.to_dfm()
    else:
        assert False, "Unknown type %s" % typ

