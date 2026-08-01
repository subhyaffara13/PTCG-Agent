
def append_invariance_notes(
    notes: list[str], arg_type: Instance, expected_type: Instance
) -> list[str]:
    """Explain that the type is invariant and give notes for how to solve the issue."""
    invariant_type = ""
    covariant_suggestion = ""
    if (
        arg_type.type.fullname == "builtins.list"
        and expected_type.type.fullname == "builtins.list"
        and is_subtype(arg_type.args[0], expected_type.args[0])
    ):
        invariant_type = "list"
        covariant_suggestion = 'Consider using "Sequence" instead, which is covariant'
    elif (
        arg_type.type.fullname == "builtins.dict"
        and expected_type.type.fullname == "builtins.dict"
        and is_same_type(arg_type.args[0], expected_type.args[0])
        and is_subtype(arg_type.args[1], expected_type.args[1])
    ):
        invariant_type = "dict"
        covariant_suggestion = (
            'Consider using "Mapping" instead, which is covariant in the value type'
        )
    if invariant_type and covariant_suggestion:
        notes.append(
            f'"{invariant_type}" is invariant -- see '
            + "https://mypy.readthedocs.io/en/stable/common_issues.html#variance"
        )
        notes.append(covariant_suggestion)
    return notes

