
def _select_dispatcher(condlist, choicelist, default=None):
    yield from condlist
    yield from choicelist

