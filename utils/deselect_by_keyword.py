
def deselect_by_keyword(items: list[Item], config: Config) -> None:
    keywordexpr = config.option.keyword.lstrip()
    if not keywordexpr:
        return

    expr = _parse_expression(keywordexpr, "Wrong expression passed to '-k'")

    remaining = []
    deselected = []
    for colitem in items:
        if not expr.evaluate(KeywordMatcher.from_item(colitem)):
            deselected.append(colitem)
        else:
            remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining

