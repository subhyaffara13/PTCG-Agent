
def _node_count(e):
    # this not only counts nodes, it affirms that the
    # args are Basic (i.e. have an args property). If
    # some object has a non-Basic arg, it needs to be
    # fixed since it is intended that all Basic args
    # are of Basic type (though this is not easy to enforce).
    if e.is_Float:
        return 0.5
    return 1 + sum(map(_node_count, e.args))

