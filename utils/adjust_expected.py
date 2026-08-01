
def adjust_expected(expected: DataFrame, read_ext: str, engine: str | None) -> None:
    expected.index.name = None
    unit = get_exp_unit(read_ext, engine)
    # error: "Index" has no attribute "as_unit"
    expected.index = expected.index.as_unit(unit)  # type: ignore[attr-defined]

