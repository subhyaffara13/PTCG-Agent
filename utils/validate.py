from typing import Any, Dict, Optional

def validate(instance, attrib, new_value):
    """
    Run *attrib*'s validator on *new_value* if it has one.

    .. versionadded:: 20.1.0
    """
    if _config._run_validators is False:
        return new_value

    v = attrib.validator
    if not v:
        return new_value

    v(instance, attrib, new_value)

    return new_value


def validate(inst):
    """
    Validate all attributes on *inst* that have a validator.

    Leaves all exceptions through.

    Args:
        inst: Instance of a class with *attrs* attributes.
    """
    if _config._run_validators is False:
        return

    for a in fields(inst.__class__):
        v = a.validator
        if v is not None:
            v(inst, a, getattr(inst, a.name))


def validate(definition, data, handlers={}, formats={}, use_default=True, use_formats=True, detailed_exceptions=True):
    """
    Validation function for lazy programmers or for use cases when you need
    to call validation only once, so you do not have to compile it first.
    Use it only when you do not care about performance (even though it will
    be still faster than alternative implementations).

    .. code-block:: python

        import fastjsonschema

        fastjsonschema.validate({'type': 'string'}, 'hello')
        # same as: compile({'type': 'string'})('hello')

    Preferred is to use :any:`compile` function.
    """
    return compile(definition, handlers, formats, use_default, use_formats, detailed_exceptions)(data)


def validate(
    regex: Pattern[bytes], data: bytes, msg: str = "malformed data", *format_args: Any
) -> Dict[str, bytes]:
    match = regex.fullmatch(data)
    if not match:
        if format_args:
            msg = msg.format(*format_args)
        raise LocalProtocolError(msg)
    return match.groupdict()


def validate(instance, schema, cls=None, *args, **kwargs):  # noqa: D417
    """
    Validate an instance under the given schema.

        >>> validate([2, 3, 4], {"maxItems": 2})
        Traceback (most recent call last):
            ...
        ValidationError: [2, 3, 4] is too long

    :func:`~jsonschema.validators.validate` will first verify that the
    provided schema is itself valid, since not doing so can lead to less
    obvious error messages and fail in less obvious or consistent ways.

    If you know you have a valid schema already, especially
    if you intend to validate multiple instances with
    the same schema, you likely would prefer using the
    `jsonschema.protocols.Validator.validate` method directly on a
    specific validator (e.g. ``Draft202012Validator.validate``).


    Arguments:

        instance:

            The instance to validate

        schema:

            The schema to validate with

        cls (jsonschema.protocols.Validator):

            The class that will be used to validate the instance.

    If the ``cls`` argument is not provided, two things will happen
    in accordance with the specification. First, if the schema has a
    :kw:`$schema` keyword containing a known meta-schema [#]_ then the
    proper validator will be used. The specification recommends that
    all schemas contain :kw:`$schema` properties for this reason. If no
    :kw:`$schema` property is found, the default validator class is the
    latest released draft.

    Any other provided positional and keyword arguments will be passed
    on when instantiating the ``cls``.

    Raises:

        `jsonschema.exceptions.ValidationError`:

            if the instance is invalid

        `jsonschema.exceptions.SchemaError`:

            if the schema itself is invalid

    .. rubric:: Footnotes
    .. [#] known by a validator registered with
        `jsonschema.validators.validates`

    """
    if cls is None:
        cls = validator_for(schema)

    cls.check_schema(schema)
    validator = cls(schema, *args, **kwargs)
    error = exceptions.best_match(validator.iter_errors(instance))
    if error is not None:
        raise error


def validate(
    nbdict: Any = None,
    ref: Optional[str] = None,
    version: Optional[int] = None,
    version_minor: Optional[int] = None,
    relax_add_props: bool = False,
    nbjson: Any = None,
    repair_duplicate_cell_ids: bool = _deprecated,  # type: ignore[assignment]
    strip_invalid_metadata: bool = _deprecated,  # type: ignore[assignment]
) -> None:
    """Checks whether the given notebook dict-like object
    conforms to the relevant notebook format schema.

    Parameters
    ----------
    nbdict : dict
        notebook document
    ref : optional, str
        reference to the subset of the schema we want to validate against.
        for example ``"markdown_cell"``, `"code_cell"` ....
    version : int
    version_minor : int
    relax_add_props : bool
        Whether to allow extra properties in the JSON schema validating the notebook.
        When True, all known fields are validated, but unknown fields are ignored.
    nbjson
    repair_duplicate_cell_ids : bool
        Deprecated since 5.5.0 - will be removed in the future.
    strip_invalid_metadata : bool
        Deprecated since 5.5.0 - will be removed in the future.

    Returns
    -------
    None

    Raises
    ------
    ValidationError if not valid.

    Notes
    -----
    Prior to Nbformat 5.5.0 the `validate` and `isvalid` method would silently
    try to fix invalid notebook and mutate arguments. This behavior is deprecated
    and will be removed in a near future.

    Please explicitly call `normalize` if you need to normalize notebooks.
    """
    assert isinstance(ref, str) or ref is None

    if strip_invalid_metadata is _deprecated:
        strip_invalid_metadata = False
    else:
        _dep_warn("strip_invalid_metadata")

    if repair_duplicate_cell_ids is _deprecated:
        repair_duplicate_cell_ids = True
    else:
        _dep_warn("repair_duplicate_cell_ids")

    # backwards compatibility for nbjson argument
    if nbdict is not None:
        pass
    elif nbjson is not None:
        nbdict = nbjson
    else:
        msg = "validate() missing 1 required argument: 'nbdict'"
        raise TypeError(msg)

    if ref is None:
        # if ref is not specified, we have a whole notebook, so we can get the version
        nbdict_version, nbdict_version_minor = get_version(nbdict)
        if version is None:
            version = nbdict_version
        if version_minor is None:
            version_minor = nbdict_version_minor
    # if ref is specified, and we don't have a version number, assume we're validating against 1.0
    elif version is None:
        version, version_minor = 1, 0

    if ref is None:
        assert isinstance(version, int)
        assert isinstance(version_minor, int)
        _normalize(
            nbdict,
            version,
            version_minor,
            repair_duplicate_cell_ids,
            relax_add_props=relax_add_props,
            strip_invalid_metadata=strip_invalid_metadata,
        )

    for error in iter_validate(
        nbdict,
        ref=ref,
        version=version,
        version_minor=version_minor,
        relax_add_props=relax_add_props,
        strip_invalid_metadata=strip_invalid_metadata,
    ):
        raise error


def validate(eps: metadata.EntryPoints):
    """
    Ensure entry points are unique by group and name and validate each.
    """
    consume(map(ensure_valid, ensure_unique(eps, key=by_group_and_name)))
    return eps


def validate(*names: Sentinel | str) -> ValidateHandler:
    """A decorator to register cross validator of HasTraits object's state
    when a Trait is set.

    The handler passed to the decorator must have one ``proposal`` dict argument.
    The proposal dictionary must hold the following keys:

    * ``owner`` : the HasTraits instance
    * ``value`` : the proposed value for the modified trait attribute
    * ``trait`` : the TraitType instance associated with the attribute

    Parameters
    ----------
    *names
        The str names of the Traits to validate.

    Notes
    -----
    Since the owner has access to the ``HasTraits`` instance via the 'owner' key,
    the registered cross validator could potentially make changes to attributes
    of the ``HasTraits`` instance. However, we recommend not to do so. The reason
    is that the cross-validation of attributes may run in arbitrary order when
    exiting the ``hold_trait_notifications`` context, and such changes may not
    commute.
    """
    if not names:
        raise TypeError("Please specify at least one trait name to validate.")
    for name in names:
        if name is not All and not isinstance(name, str):
            raise TypeError("trait names to validate must be strings or All, not %r" % name)
    return ValidateHandler(names)


def validate(*args):
    if not all(arg.is_Matrix for arg in args):
        raise TypeError("Mix of Matrix and Scalar symbols")


def validate(config: dict, filepath: StrPath) -> bool:
    from . import _validate_pyproject as validator

    trove_classifier = validator.FORMAT_FUNCTIONS.get("trove-classifier")
    if hasattr(trove_classifier, "_disable_download"):
        # Improve reproducibility by default. See abravalheri/validate-pyproject#31
        trove_classifier._disable_download()  # type: ignore[union-attr]

    try:
        return validator.validate(config)
    except validator.ValidationError as ex:
        summary = f"configuration error: {ex.summary}"
        if ex.name.strip("`") != "project":
            # Probably it is just a field missing/misnamed, not worthy the verbosity...
            _logger.debug(summary)
            _logger.debug(ex.details)

        error = f"invalid pyproject.toml config: {ex.name}."
        raise ValueError(f"{error}\n{summary}") from None


def validate(data, custom_formats={}, name_prefix=None):
    validate_https___packaging_python_org_en_latest_specifications_declaring_build_dependencies(data, custom_formats, (name_prefix or "data") + "")
    return data


def validate(data: Any) -> bool:
    """Validate the given ``data`` object using JSON Schema
    This function raises ``ValidationError`` if ``data`` is invalid.
    """
    with detailed_errors():
        _validate(data, custom_formats=FORMAT_FUNCTIONS)
        reduce(lambda acc, fn: fn(acc), EXTRA_VALIDATIONS, data)
    return True


def validate(node, ref=None):
    """validate a v4 node"""
    from nbformat import validate as validate_orig

    return validate_orig(node, ref=ref, version=nbformat)

