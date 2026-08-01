
def xfp_group(fr_grp, relators=()):
    _fp_group = FpGroup(fr_grp, relators)
    return (_fp_group, _fp_group._generators)

