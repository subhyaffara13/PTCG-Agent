
def get_all_styles():
    """Return a generator for all styles by name, both builtin and plugin."""
    for v in STYLES.values():
        yield v[1]
    for name, _ in find_plugin_styles():
        yield name


def get_all_styles():
    """Return a generator for all styles by name, both builtin and plugin."""
    for v in STYLES.values():
        yield v[1]
    for name, _ in find_plugin_styles():
        yield name

