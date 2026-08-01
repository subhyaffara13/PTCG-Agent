
def _eval_cond(cond):
    """ Re-evaluate the conditions. """
    if isinstance(cond, bool):
        return cond
    return _condsimp(cond.doit())

