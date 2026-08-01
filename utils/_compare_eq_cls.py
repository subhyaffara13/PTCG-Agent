
def _compare_eq_cls(
    left: object,
    right: object,
    highlighter: _HighlightFunc,
    verbose: int,
    assertion_text_diff_style: _AssertionTextDiffStyle,
) -> Iterator[str]:
    if not has_default_eq(left):
        return
    if isdatacls(left):
        all_fields = dataclasses.fields(left)
        fields_to_check = [info.name for info in all_fields if info.compare]
    elif isattrs(left):
        all_fields = left.__attrs_attrs__  # type: ignore[attr-defined]
        fields_to_check = [field.name for field in all_fields if getattr(field, "eq")]
    elif isnamedtuple(left):
        fields_to_check = left._fields  # type: ignore[attr-defined]
    else:
        assert False

    indent = "  "
    same = []
    diff = []
    for field in fields_to_check:
        if getattr(left, field) == getattr(right, field):
            same.append(field)
        else:
            diff.append(field)

    if same or diff:
        yield ""
    if same and verbose < 2:
        yield f"Omitting {len(same)} identical items, use -vv to show"
    elif same:
        yield "Matching attributes:"
        yield from highlighter(pprint.pformat(same)).splitlines()
    if diff:
        yield "Differing attributes:"
        yield from highlighter(pprint.pformat(diff)).splitlines()
        for field in diff:
            field_left = getattr(left, field)
            field_right = getattr(right, field)
            yield ""
            yield f"Drill down into differing attribute {field}:"
            yield f"{indent}{field}: {highlighter(repr(field_left))} != {highlighter(repr(field_right))}"
            for line in _compare_eq_any(
                field_left,
                field_right,
                highlighter,
                verbose,
                assertion_text_diff_style,
            ):
                yield indent + line

