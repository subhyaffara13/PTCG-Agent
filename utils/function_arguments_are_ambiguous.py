
def function_arguments_are_ambiguous(
    func1: nodes.FunctionDef, func2: nodes.FunctionDef
) -> bool:
    if func1.argnames() != func2.argnames():
        return True
    # Check ambiguity among function default values
    pairs_of_defaults = [
        (func1.args.defaults, func2.args.defaults),
        (func1.args.kw_defaults, func2.args.kw_defaults),
    ]
    for zippable_default in pairs_of_defaults:
        if None in zippable_default:
            continue
        if len(zippable_default[0]) != len(zippable_default[1]):
            return True
        for default1, default2 in zip(*zippable_default):
            match (default1, default2):
                case [nodes.Const(), nodes.Const()]:
                    return default1.value != default2.value  # type: ignore[no-any-return]
                case [nodes.Name(), nodes.Name()]:
                    return default1.name != default2.name  # type: ignore[no-any-return]
                case _:
                    return True
    return False

