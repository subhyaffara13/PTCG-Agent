
def _folded_skips(
    startpath: Path,
    skipped: Sequence[CollectReport],
) -> list[tuple[int, str, int | None, str]]:
    d: dict[tuple[str, int | None, str], list[CollectReport]] = {}
    for event in skipped:
        assert event.longrepr is not None
        assert isinstance(event.longrepr, tuple), (event, event.longrepr)
        assert len(event.longrepr) == 3, (event, event.longrepr)
        fspath, lineno, reason = event.longrepr
        # For consistency, report all fspaths in relative form.
        fspath = bestrelpath(startpath, Path(fspath))
        keywords = getattr(event, "keywords", {})
        # Folding reports with global pytestmark variable.
        # This is a workaround, because for now we cannot identify the scope of a skip marker
        # TODO: Revisit after marks scope would be fixed.
        if (
            event.when == "setup"
            and "skip" in keywords
            and "pytestmark" not in keywords
        ):
            key: tuple[str, int | None, str] = (fspath, None, reason)
        else:
            key = (fspath, lineno, reason)
        d.setdefault(key, []).append(event)
    values: list[tuple[int, str, int | None, str]] = []
    for key, events in d.items():
        values.append((len(events), *key))
    return values

