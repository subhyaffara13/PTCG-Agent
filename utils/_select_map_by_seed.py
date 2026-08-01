
def _select_map_by_seed(seed):
    """Pick a built-in map name. None picks randomly; otherwise deterministic."""
    names = sorted(BUILTIN_MAPS)
    if seed is None:
        return names[np.random.randint(0, len(names))]
    return names[int(seed) % len(names)]

