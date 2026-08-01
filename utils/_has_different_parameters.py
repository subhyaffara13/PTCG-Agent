
def _has_different_parameters(
    original: list[nodes.AssignName],
    overridden: list[nodes.AssignName],
    dummy_parameter_regex: Pattern[str],
) -> list[str]:
    result: list[str] = []
    zipped = zip_longest(original, overridden)
    for original_param, overridden_param in zipped:
        if not overridden_param:
            return ["Number of parameters "]

        if not original_param:
            try:
                overridden_param.parent.default_value(overridden_param.name)
                continue
            except astroid.NoDefault:
                return ["Number of parameters "]

        # check for the arguments' name
        names = [param.name for param in (original_param, overridden_param)]
        if any(dummy_parameter_regex.match(name) for name in names):
            continue
        if original_param.name != overridden_param.name:
            result.append(
                f"Parameter '{original_param.name}' has been renamed "
                f"to '{overridden_param.name}' in"
            )

    return result

