
def _flake8_plugins(
    eps: Iterable[importlib.metadata.EntryPoint],
    name: str,
    version: str,
) -> Generator[Plugin]:
    pyflakes_meta = importlib.metadata.distribution("pyflakes").metadata
    pycodestyle_meta = importlib.metadata.distribution("pycodestyle").metadata

    for ep in eps:
        if ep.group not in FLAKE8_GROUPS:
            continue

        if ep.name == "F":
            yield Plugin(pyflakes_meta["name"], pyflakes_meta["version"], ep)
        elif ep.name in "EW":
            # pycodestyle provides both `E` and `W` -- but our default select
            # handles those
            # ideally pycodestyle's plugin entrypoints would exactly represent
            # the codes they produce...
            yield Plugin(
                pycodestyle_meta["name"], pycodestyle_meta["version"], ep
            )
        else:
            yield Plugin(name, version, ep)

