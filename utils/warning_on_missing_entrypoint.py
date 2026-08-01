
def warning_on_missing_entrypoint(missing_names: Iterable[str]) -> None:
    LOG.warning('Could not load %s', ', '.join(missing_names))

