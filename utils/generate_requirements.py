
def generate_requirements(
    extras_require: dict[str | None, list[str]],
) -> Iterator[tuple[str, str]]:
    """
    Convert requirements from a setup()-style dictionary to
    ('Requires-Dist', 'requirement') and ('Provides-Extra', 'extra') tuples.

    extras_require is a dictionary of {extra: [requirements]} as passed to setup(),
    using the empty extra {'': [requirements]} to hold install_requires.
    """
    for extra, depends in extras_require.items():
        condition = ""
        extra = extra or ""
        if ":" in extra:  # setuptools extra:condition syntax
            extra, condition = extra.split(":", 1)

        extra = safe_extra(extra)
        if extra:
            yield "Provides-Extra", extra
            if condition:
                condition = "(" + condition + ") and "
            condition += f"extra == '{extra}'"

        if condition:
            condition = " ; " + condition

        for new_req in convert_requirements(depends):
            canonical_req = str(Requirement(new_req + condition))
            yield "Requires-Dist", canonical_req

