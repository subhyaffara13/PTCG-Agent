
def validator_for(
    schema,
    default: type[Validator] | _utils.Unset = _UNSET,
) -> type[Validator]:
    """
    Retrieve the validator class appropriate for validating the given schema.

    Uses the :kw:`$schema` keyword that should be present in the given
    schema to look up the appropriate validator class.

    Arguments:

        schema (collections.abc.Mapping or bool):

            the schema to look at

        default:

            the default to return if the appropriate validator class
            cannot be determined.

            If unprovided, the default is to return the latest supported
            draft.

    Examples:

        The :kw:`$schema` JSON Schema keyword will control which validator
        class is returned:

        >>> schema = {
        ...     "$schema": "https://json-schema.org/draft/2020-12/schema",
        ...     "type": "integer",
        ... }
        >>> jsonschema.validators.validator_for(schema)
        <class 'jsonschema.validators.Draft202012Validator'>


        Here, a draft 7 schema instead will return the draft 7 validator:

        >>> schema = {
        ...     "$schema": "http://json-schema.org/draft-07/schema#",
        ...     "type": "integer",
        ... }
        >>> jsonschema.validators.validator_for(schema)
        <class 'jsonschema.validators.Draft7Validator'>


        Schemas with no ``$schema`` keyword will fallback to the default
        argument:

        >>> schema = {"type": "integer"}
        >>> jsonschema.validators.validator_for(
        ...     schema, default=Draft7Validator,
        ... )
        <class 'jsonschema.validators.Draft7Validator'>

        or if none is provided, to the latest version supported.
        Always including the keyword when authoring schemas is highly
        recommended.

    """
    DefaultValidator = _LATEST_VERSION if default is _UNSET else default

    if schema is True or schema is False or "$schema" not in schema:
        return DefaultValidator  # type: ignore[return-value]
    if schema["$schema"] not in _META_SCHEMAS and default is _UNSET:
        warn(
            (
                "The metaschema specified by $schema was not found. "
                "Using the latest draft to validate, but this will raise "
                "an error in the future."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
    return _META_SCHEMAS.get(schema["$schema"], DefaultValidator)

