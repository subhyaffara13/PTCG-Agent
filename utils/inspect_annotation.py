
def inspect_annotation(  # noqa: PLR0915
    annotation: Any,
    /,
    *,
    annotation_source: AnnotationSource,
    unpack_type_aliases: Literal['skip', 'lenient', 'eager'] = 'skip',
) -> InspectedAnnotation:
    """Inspect an [annotation expression][], extracting any [type qualifier][] and metadata.

    An [annotation expression][] is a [type expression][] optionally surrounded by one or more
    [type qualifiers][type qualifier] or by [`Annotated`][typing.Annotated]. This function will:

    - Unwrap the type expression, keeping track of the type qualifiers.
    - Unwrap [`Annotated`][typing.Annotated] forms, keeping track of the annotated metadata.

    Args:
        annotation: The annotation expression to be inspected.
        annotation_source: The source of the annotation. Depending on the source (e.g. a class), different type
            qualifiers may be (dis)allowed. To allow any type qualifier, use
            [`AnnotationSource.ANY`][typing_inspection.introspection.AnnotationSource.ANY].
        unpack_type_aliases: What to do when encountering [PEP 695](https://peps.python.org/pep-0695/)
            [type aliases][type-aliases]. Can be one of:

            - `'skip'`: Do not try to parse type aliases (the default):
              ```pycon
              >>> type MyInt = Annotated[int, 'meta']
              >>> inspect_annotation(MyInt, annotation_source=AnnotationSource.BARE, unpack_type_aliases='skip')
              InspectedAnnotation(type=MyInt, qualifiers={}, metadata=[])
              ```

            - `'lenient'`: Try to parse type aliases, and fallback to `'skip'` if the type alias
              can't be inspected (because of an undefined forward reference):
              ```pycon
              >>> type MyInt = Annotated[Undefined, 'meta']
              >>> inspect_annotation(MyInt, annotation_source=AnnotationSource.BARE, unpack_type_aliases='lenient')
              InspectedAnnotation(type=MyInt, qualifiers={}, metadata=[])
              >>> Undefined = int
              >>> inspect_annotation(MyInt, annotation_source=AnnotationSource.BARE, unpack_type_aliases='lenient')
              InspectedAnnotation(type=int, qualifiers={}, metadata=['meta'])
              ```

            - `'eager'`: Parse type aliases and raise any encountered [`NameError`][] exceptions.

    Returns:
        The result of the inspected annotation, where the type expression, used qualifiers and metadata is stored.

    Example:
        ```pycon
        >>> inspect_annotation(
        ...     Final[Annotated[ClassVar[Annotated[int, 'meta_1']], 'meta_2']],
        ...     annotation_source=AnnotationSource.CLASS,
        ... )
        ...
        InspectedAnnotation(type=int, qualifiers={'class_var', 'final'}, metadata=['meta_1', 'meta_2'])
        ```
    """
    allowed_qualifiers = annotation_source.allowed_qualifiers
    qualifiers: set[Qualifier] = set()
    metadata: list[Any] = []

    while True:
        annotation, _meta = _unpack_annotated(annotation, unpack_type_aliases=unpack_type_aliases)
        if _meta:
            metadata = _meta + metadata
            continue

        origin = get_origin(annotation)
        if origin is not None:
            if typing_objects.is_classvar(origin):
                if 'class_var' not in allowed_qualifiers:
                    raise ForbiddenQualifier('class_var')
                qualifiers.add('class_var')
                annotation = annotation.__args__[0]
            elif typing_objects.is_final(origin):
                if 'final' not in allowed_qualifiers:
                    raise ForbiddenQualifier('final')
                qualifiers.add('final')
                annotation = annotation.__args__[0]
            elif typing_objects.is_required(origin):
                if 'required' not in allowed_qualifiers:
                    raise ForbiddenQualifier('required')
                qualifiers.add('required')
                annotation = annotation.__args__[0]
            elif typing_objects.is_notrequired(origin):
                if 'not_required' not in allowed_qualifiers:
                    raise ForbiddenQualifier('not_required')
                qualifiers.add('not_required')
                annotation = annotation.__args__[0]
            elif typing_objects.is_readonly(origin):
                if 'read_only' not in allowed_qualifiers:
                    raise ForbiddenQualifier('not_required')
                qualifiers.add('read_only')
                annotation = annotation.__args__[0]
            else:
                # origin is not None but not a type qualifier nor `Annotated` (e.g. `list[int]`):
                break
        elif isinstance(annotation, InitVar):
            if 'init_var' not in allowed_qualifiers:
                raise ForbiddenQualifier('init_var')
            qualifiers.add('init_var')
            annotation = cast(Any, annotation.type)
        else:
            break

    # `Final`, `ClassVar` and `InitVar` are type qualifiers allowed to be used as a bare annotation:
    if typing_objects.is_final(annotation):
        if 'final' not in allowed_qualifiers:
            raise ForbiddenQualifier('final')
        qualifiers.add('final')
        annotation = UNKNOWN
    elif typing_objects.is_classvar(annotation):
        if 'class_var' not in allowed_qualifiers:
            raise ForbiddenQualifier('class_var')
        qualifiers.add('class_var')
        annotation = UNKNOWN
    elif annotation is InitVar:
        if 'init_var' not in allowed_qualifiers:
            raise ForbiddenQualifier('init_var')
        qualifiers.add('init_var')
        annotation = UNKNOWN

    return InspectedAnnotation(annotation, qualifiers, metadata)

