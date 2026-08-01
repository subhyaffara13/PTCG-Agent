
def get_validator(version=None, version_minor=None, relax_add_props=False, name=None):
    """Load the JSON schema into a Validator"""
    if version is None:
        from . import current_nbformat

        version = current_nbformat

    v = import_item("nbformat.v%s" % version)
    current_minor = getattr(v, "nbformat_minor", 0)
    if version_minor is None:
        version_minor = current_minor

    current_validator = _validator_for_name(name) if name else get_current_validator()

    version_tuple = (current_validator.name, version, version_minor)

    if version_tuple not in validators:
        try:
            schema_json = _get_schema_json(v, version=version, version_minor=version_minor)
        except AttributeError:
            return None

        if current_minor < version_minor:
            # notebook from the future, relax all `additionalProperties: False` requirements
            schema_json = _relax_additional_properties(schema_json)
            # and allow undefined cell types and outputs
            schema_json = _allow_undefined(schema_json)

        validators[version_tuple] = current_validator(schema_json)

    if relax_add_props:
        try:
            schema_json = _get_schema_json(v, version=version, version_minor=version_minor)
        except AttributeError:
            return None

        # this allows properties to be added for intermediate
        # representations while validating for all other kinds of errors
        schema_json = _relax_additional_properties(schema_json)
        validators[version_tuple] = current_validator(schema_json)

    return validators[version_tuple]

