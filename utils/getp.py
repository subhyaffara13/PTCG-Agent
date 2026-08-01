
def getp(obj, property=None):
    """
    Return the value of an `.Artist`'s *property*, or print all of them.

    Parameters
    ----------
    obj : `~matplotlib.artist.Artist`
        The queried artist; e.g., a `.Line2D`, a `.Text`, or an `~.axes.Axes`.

    property : str or None, default: None
        If *property* is 'somename', this function returns
        ``obj.get_somename()``.

        If it's None (or unset), it *prints* all gettable properties from
        *obj*.  Many properties have aliases for shorter typing, e.g. 'lw' is
        an alias for 'linewidth'.  In the output, aliases and full property
        names will be listed as:

          property or alias = value

        e.g.:

          linewidth or lw = 2

    See Also
    --------
    setp
    """
    if property is None:
        insp = ArtistInspector(obj)
        ret = insp.pprint_getters()
        print('\n'.join(ret))
        return
    return getattr(obj, 'get_' + property)()


def getp(obj, *args, **kwargs):
    return matplotlib.artist.getp(obj, *args, **kwargs)

