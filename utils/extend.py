
def extend(use_dill=True):
    '''add (or remove) dill types to/from the pickle registry

    by default, ``dill`` populates its types to ``pickle.Pickler.dispatch``.
    Thus, all ``dill`` types are available upon calling ``'import pickle'``.
    To drop all ``dill`` types from the ``pickle`` dispatch, *use_dill=False*.

    Args:
        use_dill (bool, default=True): if True, extend the dispatch table.

    Returns:
        None
    '''
    from ._dill import _revert_extension, _extend
    if use_dill: _extend()
    else: _revert_extension()
    return


def extend(
    validator,
    validators=(),
    version=None,
    type_checker=None,
    format_checker=None,
):
    """
    Create a new validator class by extending an existing one.

    Arguments:

        validator (jsonschema.protocols.Validator):

            an existing validator class

        validators (collections.abc.Mapping):

            a mapping of new validator callables to extend with, whose
            structure is as in `create`.

            .. note::

                Any validator callables with the same name as an
                existing one will (silently) replace the old validator
                callable entirely, effectively overriding any validation
                done in the "parent" validator class.

                If you wish to instead extend the behavior of a parent's
                validator callable, delegate and call it directly in
                the new validator function by retrieving it using
                ``OldValidator.VALIDATORS["validation_keyword_name"]``.

        version (str):

            a version for the new validator class

        type_checker (jsonschema.TypeChecker):

            a type checker, used when applying the :kw:`type` keyword.

            If unprovided, the type checker of the extended
            `jsonschema.protocols.Validator` will be carried along.

        format_checker (jsonschema.FormatChecker):

            a format checker, used when applying the :kw:`format` keyword.

            If unprovided, the format checker of the extended
            `jsonschema.protocols.Validator` will be carried along.

    Returns:

        a new `jsonschema.protocols.Validator` class extending the one
        provided

    .. note:: Meta Schemas

        The new validator class will have its parent's meta schema.

        If you wish to change or extend the meta schema in the new
        validator class, modify ``META_SCHEMA`` directly on the returned
        class. Note that no implicit copying is done, so a copy should
        likely be made before modifying it, in order to not affect the
        old validator.

    """
    all_validators = dict(validator.VALIDATORS)
    all_validators.update(validators)

    if type_checker is None:
        type_checker = validator.TYPE_CHECKER
    if format_checker is None:
        format_checker = validator.FORMAT_CHECKER
    return create(
        meta_schema=validator.META_SCHEMA,
        validators=all_validators,
        version=version,
        type_checker=type_checker,
        format_checker=format_checker,
        id_of=validator.ID_OF,
        applicable_validators=validator._APPLICABLE_VALIDATORS,
    )

