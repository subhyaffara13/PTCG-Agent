
def _suppress_lower_units(min_unit: Unit, suppress: Iterable[Unit]) -> set[Unit]:
    """Extend suppressed units (if any) with all units lower than the minimum unit.

    >>> from humanize.time import _suppress_lower_units, Unit
    >>> [x.name for x in sorted(_suppress_lower_units(Unit.SECONDS, [Unit.DAYS]))]
    ['MICROSECONDS', 'MILLISECONDS', 'DAYS']
    """
    suppress = set(suppress)
    for unit in Unit:
        if unit == min_unit:
            break
        suppress.add(unit)

    return suppress

