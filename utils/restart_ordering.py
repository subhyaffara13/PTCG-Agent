
def restart_ordering(on_ambiguity=ambiguity_warn):
    """Deprecated interface to temporarily resume ordering."""


def restart_ordering(on_ambiguity=ambiguity_warn):
    _resolve[0] = True
    while _unresolved_dispatchers:
        dispatcher = _unresolved_dispatchers.pop()
        dispatcher.reorder(on_ambiguity=on_ambiguity)

