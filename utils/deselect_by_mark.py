
def deselect_by_mark(items: list[Item], config: Config) -> None:
    matchexpr = config.option.markexpr
    if not matchexpr:
        return

    expr = _parse_expression(matchexpr, "Wrong expression passed to '-m'")
    remaining: list[Item] = []
    deselected: list[Item] = []
    for item in items:
        if expr.evaluate(MarkMatcher.from_markers(item.iter_markers())):
            remaining.append(item)
        else:
            deselected.append(item)
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining

