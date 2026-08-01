
def rec_join(key, r1, r2, jointype='inner', r1postfix='1', r2postfix='2',
             defaults=None):
    """
    Join arrays `r1` and `r2` on keys.
    Alternative to join_by, that always returns a np.recarray.

    See Also
    --------
    join_by : equivalent function
    """
    kwargs = {'jointype': jointype, 'r1postfix': r1postfix, 'r2postfix': r2postfix,
                  'defaults': defaults, 'usemask': False, 'asrecarray': True}
    return join_by(key, r1, r2, **kwargs)

