
def make_literal_validator(type_: Any) -> Callable[[Any], Any]:
    permitted_choices = all_literal_values(type_)

    # To have a O(1) complexity and still return one of the values set inside the `Literal`,
    # we create a dict with the set values (a set causes some problems with the way intersection works).
    # In some cases the set value and checked value can indeed be different (see `test_literal_validator_str_enum`)
    allowed_choices = {v: v for v in permitted_choices}

    def literal_validator(v: Any) -> Any:
        try:
            return allowed_choices[v]
        except (KeyError, TypeError):
            raise errors.WrongConstantError(given=v, permitted=permitted_choices)

    return literal_validator

