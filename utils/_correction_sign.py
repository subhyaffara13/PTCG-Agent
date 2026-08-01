
def _correction_sign(z, alternative, xp):
    if alternative == 'greater':
        return 1
    elif alternative == 'less':
        return -1
    else:
        return xp.sign(z)

