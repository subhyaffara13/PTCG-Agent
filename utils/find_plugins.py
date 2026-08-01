
def find_plugins(
    cfg: configparser.RawConfigParser,
    opts: PluginOptions,
) -> list[Plugin]:
    """Discovers all plugins (but does not load them)."""
    ret = [*_find_importlib_plugins(), *_find_local_plugins(cfg)]

    # for determinism, sort the list
    ret.sort()

    _check_required_plugins(ret, opts.require_plugins)

    return ret

