
def get_model_type_hints(
    model_class: type[BaseModel],
    *,
    ns_resolver: NsResolver | None = None,
) -> dict[str, tuple[Any, bool]]:
    """Collect annotations from a Pydantic model class, including those from parent classes.

    Args:
        model_class: The Pydantic model class to inspect.
        ns_resolver: A namespace resolver instance to use. Defaults to an empty instance.

    Returns:
        A dictionary mapping annotation names to a two-tuple: the first element is the evaluated
        type or the original annotation if a `NameError` occurred, the second element is a boolean
        indicating if whether the evaluation succeeded.
    """
    hints: dict[str, Any] | dict[str, tuple[Any, bool]] = {}
    ns_resolver = ns_resolver or NsResolver()

    for base in reversed(model_class.__mro__[:-1]):
        # For Python 3.14, we could also use `Format.VALUE` and pass the globals/locals
        # from the ns_resolver, but we want to be able to know which specific field failed
        # to evaluate:
        ann = safe_get_annotations(base)

        if not ann:
            continue

        with ns_resolver.push(base):
            base_model_fields: dict[str, FieldInfo] | None = base.__dict__.get('__pydantic_fields__')

            for name, value in ann.items():
                if name.startswith('_'):
                    globalns, localns = ns_resolver.types_namespace

                    # For private attributes, we only need the annotation to detect the `ClassVar` special form.
                    # For this reason, we still try to evaluate it, but we also catch any possible exception (on
                    # top of the `NameError`s caught in `try_eval_type`) that could happen so that users are free
                    # to use any kind of forward annotation for private fields (e.g. circular imports, new typing
                    # syntax, etc).
                    try:
                        hints[name] = try_eval_type(value, globalns, localns)
                    except Exception:
                        hints[name] = (value, False)
                else:
                    if base_model_fields is not None and name in base_model_fields:
                        # Avoid unnecessarily evaluating annotations from parent models, as we'll end up
                        # copying the `FieldInfo` instance from it anyway if we need to.
                        # We use the `annotation` attribute here, but in reality could put anything here,
                        # As we are guaranteed to not make use of it:
                        hints[name] = (base_model_fields[name].annotation, True)
                    else:
                        globalns, localns = ns_resolver.types_namespace

                        hints[name] = try_eval_type(value, globalns, localns)

    return hints

