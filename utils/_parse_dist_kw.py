
def _parse_dist_kw(dist, enforce_subclass=True):
    """Parse `dist` keyword.

    Parameters
    ----------
    dist : str or stats.distributions instance.
        Several functions take `dist` as a keyword, hence this utility
        function.
    enforce_subclass : bool, optional
        If True (default), `dist` needs to be a
        `_distn_infrastructure.rv_generic` instance.
        It can sometimes be useful to set this keyword to False, if a function
        wants to accept objects that just look somewhat like such an instance
        (for example, they have a ``ppf`` method).

    """
    if isinstance(dist, rv_generic):
        pass
    elif isinstance(dist, str):
        try:
            dist = getattr(distributions, dist)
        except AttributeError as e:
            raise ValueError(f"{dist} is not a valid distribution name") from e
    elif enforce_subclass:
        msg = ("`dist` should be a stats.distributions instance or a string "
               "with the name of such a distribution.")
        raise ValueError(msg)

    return dist

