import sys

def _build_cacheable_data() -> _CacheEntry:
    entry_points = importlib.metadata.entry_points()
    groups: dict[str, list[tuple[str, str, str]]] = {}
    for group in entry_points.groups:
        existing = set()
        groups[group] = []
        for ep in entry_points.select(group=group):
            # Filter out duplicates that can occur when testing a
            # package that provides entry points using tox, where the
            # package is installed in the virtualenv that tox builds
            # and is present in the path as '.'.
            item = ep.name, ep.value, ep.group  # convert to tuple
            if item in existing:
                continue
            existing.add(item)
            groups[group].append(item)

    return {
        'groups': groups,
        'sys.executable': sys.executable,
        'sys.prefix': sys.prefix,
        'path_values': [],
    }

