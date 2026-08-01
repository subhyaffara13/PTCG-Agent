
def _find_importlib_plugins() -> Generator[Plugin]:
    # some misconfigured pythons (RHEL) have things on `sys.path` twice
    seen = set()
    for dist in importlib.metadata.distributions():
        # assigned to prevent continual reparsing
        eps = dist.entry_points

        # perf: skip parsing `.metadata` (slow) if no entry points match
        if not any(ep.group in FLAKE8_GROUPS for ep in eps):
            continue

        # assigned to prevent continual reparsing
        meta = dist.metadata

        if meta["name"] in seen:
            continue
        else:
            seen.add(meta["name"])

        if meta["name"] in BANNED_PLUGINS:
            LOG.warning(
                "%s plugin is obsolete in flake8>=%s",
                meta["name"],
                BANNED_PLUGINS[meta["name"]],
            )
            continue
        elif meta["name"] == "flake8":
            # special case flake8 which provides plugins for pyflakes /
            # pycodestyle
            yield from _flake8_plugins(eps, meta["name"], meta["version"])
            continue

        for ep in eps:
            if ep.group in FLAKE8_GROUPS:
                yield Plugin(meta["name"], meta["version"], ep)

