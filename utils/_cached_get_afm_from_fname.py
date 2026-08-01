
def _cached_get_afm_from_fname(fname):
    with open(fname, "rb") as fh:
        return AFM(fh)

