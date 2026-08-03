from typing import Callable

def _apply_alias_generator_to_field_info(
    alias_generator: Callable[[str], str] | AliasGenerator, field_name: str, field_info: FieldInfo
):
    """Apply an alias generator to aliases on a `FieldInfo` instance if appropriate.

    Args:
        alias_generator: A callable that takes a string and returns a string, or an `AliasGenerator` instance.
        field_name: The name of the field from which to generate the alias.
        field_info: The `FieldInfo` instance to which the alias generator is (maybe) applied.
    """
    # Apply an alias_generator if
    # 1. An alias is not specified
    # 2. An alias is specified, but the priority is <= 1
    if (
        field_info.alias_priority is None
        or field_info.alias_priority <= 1
        or field_info.alias is None
        or field_info.validation_alias is None
        or field_info.serialization_alias is None
    ):
        alias, validation_alias, serialization_alias = None, None, None

        if isinstance(alias_generator, AliasGenerator):
            alias, validation_alias, serialization_alias = alias_generator.generate_aliases(field_name)
        elif callable(alias_generator):
            alias = alias_generator(field_name)
            if not isinstance(alias, str):
                raise TypeError(f'alias_generator {alias_generator} must return str, not {alias.__class__}')

        # if priority is not set, we set to 1
        # which supports the case where the alias_generator from a child class is used
        # to generate an alias for a field in a parent class
        if field_info.alias_priority is None or field_info.alias_priority <= 1:
            field_info.alias_priority = 1

        # if the priority is 1, then we set the aliases to the generated alias
        if field_info.alias_priority == 1:
            field_info.serialization_alias = get_first_not_none(serialization_alias, alias)
            field_info.validation_alias = get_first_not_none(validation_alias, alias)
            field_info.alias = alias

        # if any of the aliases are not set, then we set them to the corresponding generated alias
        if field_info.alias is None:
            field_info.alias = alias
        if field_info.serialization_alias is None:
            field_info.serialization_alias = get_first_not_none(serialization_alias, alias)
        if field_info.validation_alias is None:
            field_info.validation_alias = get_first_not_none(validation_alias, alias)

