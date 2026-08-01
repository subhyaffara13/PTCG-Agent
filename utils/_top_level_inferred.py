
def _top_level_inferred(dist):
    opt_names = set(map(_get_toplevel_name, always_iterable(dist.files)))

    def importable_name(name):
        return '.' not in name

    return filter(importable_name, opt_names)


def _top_level_inferred(dist):
    opt_names = set(map(_get_toplevel_name, always_iterable(dist.files)))

    def importable_name(name):
        return '.' not in name

    return filter(importable_name, opt_names)

