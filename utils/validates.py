
def validates(version):
    """
    Register the decorated validator for a ``version`` of the specification.

    Registered validators and their meta schemas will be considered when
    parsing :kw:`$schema` keywords' URIs.

    Arguments:

        version (str):

            An identifier to use as the version's name

    Returns:

        collections.abc.Callable:

            a class decorator to decorate the validator with the version

    """

    def _validates(cls):
        _VALIDATORS[version] = cls
        meta_schema_id = cls.ID_OF(cls.META_SCHEMA)
        _META_SCHEMAS[meta_schema_id] = cls
        return cls
    return _validates

