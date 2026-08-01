
def collect_model_fields(  # noqa: C901
    cls: type[BaseModel],
    config_wrapper: ConfigWrapper,
    ns_resolver: NsResolver,
    *,
    typevars_map: Mapping[TypeVar, Any] | None = None,
) -> tuple[dict[str, FieldInfo], PydanticExtraInfo | None, set[str]]:
    """Collect the fields and class variables names of a nascent Pydantic model.

    The fields collection process is *lenient*, meaning it won't error if string annotations
    fail to evaluate. If this happens, the original annotation (and assigned value, if any)
    is stored on the created `FieldInfo` instance.

    The `rebuild_model_fields()` should be called at a later point (e.g. when rebuilding the model),
    and will make use of these stored attributes.

    Args:
        cls: BaseModel or dataclass.
        config_wrapper: The config wrapper instance.
        ns_resolver: Namespace resolver to use when getting model annotations.
        typevars_map: A dictionary mapping type variables to their concrete types.

    Returns:
        A three-tuple containing the model fields, the `PydanticExtraInfo` instance if the `__pydantic_extra__` annotation is set,
        and class variables names.

    Raises:
        NameError:
            - If there is a conflict between a field name and protected namespaces.
            - If there is a field other than `root` in `RootModel`.
            - If a field shadows an attribute in the parent model.
    """
    FieldInfo_ = import_cached_field_info()
    BaseModel_ = import_cached_base_model()

    bases = cls.__bases__
    parent_fields_lookup: dict[str, FieldInfo] = {}
    for base in reversed(bases):
        if model_fields := getattr(base, '__pydantic_fields__', None):
            parent_fields_lookup.update(model_fields)

    type_hints = _typing_extra.get_model_type_hints(cls, ns_resolver=ns_resolver)

    # `cls_annotations` is only used to determine if an annotation comes from a parent class
    cls_annotations = _typing_extra.safe_get_annotations(cls)

    fields: dict[str, FieldInfo] = {}

    class_vars: set[str] = set()
    for ann_name, (ann_type, evaluated) in type_hints.items():
        if ann_name == 'model_config':
            # We never want to treat `model_config` as a field
            # Note: we may need to change this logic if/when we introduce a `BareModel` class with no
            # protected namespaces (where `model_config` might be allowed as a field name)
            continue

        _check_protected_namespaces(
            protected_namespaces=config_wrapper.protected_namespaces,
            ann_name=ann_name,
            bases=bases,
            cls_name=cls.__name__,
        )

        if _typing_extra.is_classvar_annotation(ann_type):
            class_vars.add(ann_name)
            continue

        assigned_value = getattr(cls, ann_name, PydanticUndefined)
        if assigned_value is not PydanticUndefined and (
            # One of the deprecated instance methods was used as a field name (e.g. `dict()`):
            any(getattr(BaseModel_, depr_name, None) is assigned_value for depr_name in _deprecated_method_names)
            # One of the deprecated class methods was used as a field name (e.g. `schema()`):
            or (
                hasattr(assigned_value, '__func__')
                and any(
                    getattr(getattr(BaseModel_, depr_name, None), '__func__', None) is assigned_value.__func__  # pyright: ignore[reportAttributeAccessIssue]
                    for depr_name in _deprecated_classmethod_names
                )
            )
        ):
            # Then `assigned_value` would be the method, even though no default was specified:
            assigned_value = PydanticUndefined

        if not is_valid_field_name(ann_name):
            continue
        if cls.__pydantic_root_model__ and ann_name != 'root':
            raise NameError(
                f"Unexpected field with name {ann_name!r}; only 'root' is allowed as a field of a `RootModel`"
            )

        for base in bases:
            if hasattr(base, ann_name):
                if ann_name not in cls_annotations:
                    # Don't warn when a field exists in a parent class but has not been defined in the current class
                    continue

                # when building a generic model with `MyModel[int]`, the generic_origin check makes sure we don't get
                # "... shadows an attribute" warnings
                generic_origin = getattr(cls, '__pydantic_generic_metadata__', {}).get('origin')
                if base is generic_origin:
                    # Don't warn when "shadowing" of attributes in parametrized generics
                    continue

                dataclass_fields = {
                    field.name for field in (dataclasses.fields(base) if dataclasses.is_dataclass(base) else ())
                }
                if ann_name in dataclass_fields:
                    # Don't warn when inheriting stdlib dataclasses whose fields are "shadowed" by defaults being set
                    # on the class instance.
                    continue

                warnings.warn(
                    f'Field name "{ann_name}" in "{cls.__qualname__}" shadows an attribute in parent '
                    f'"{base.__qualname__}"',
                    UserWarning,
                    stacklevel=4,
                )

        if assigned_value is PydanticUndefined:  # no assignment, just a plain annotation
            if ann_name in cls_annotations or ann_name not in parent_fields_lookup:
                # field is either:
                # - present in the current model's annotations (and *not* from parent classes)
                # - not found on any base classes; this seems to be caused by fields not getting
                #   generated due to models not being fully defined while initializing recursive models.
                #   Nothing stops us from just creating a `FieldInfo` for this type hint, so we do this.
                field_info = FieldInfo_.from_annotation(ann_type, _source=AnnotationSource.CLASS)
                field_info._original_annotation = ann_type
                if not evaluated:
                    field_info._complete = False
                    # Store the original annotation that should be used to rebuild
                    # the field info later:
            else:
                # The field was present on one of the (possibly multiple) base classes, we make a copy directly from it.
                parent_field_info = parent_fields_lookup[ann_name]._copy()

                # The only case where substituting the type variables is relevant (i.e. when `typevars_map` is not empty)
                # is when a generic class is parameterized (e.g. `MyGenericModel[int, str]`), which creates a new class object
                # (unlike the stdlib genercis that create a generic alias). In this case, we are guaranteed to only have to copy
                # from the origin/parent model (e.g. `MyGenericModel`).
                if typevars_map:
                    field_info = _recreate_field_info(
                        parent_field_info, ns_resolver=ns_resolver, typevars_map=typevars_map, lenient=True
                    )
                else:
                    field_info = parent_field_info

        else:  # An assigned value is present (either the default value, or a `Field()` function)
            if isinstance(assigned_value, FieldInfo_) and ismethoddescriptor(assigned_value.default):
                # `assigned_value` was fetched using `getattr`, which triggers a call to `__get__`
                # for descriptors, so we do the same if the `= field(default=...)` form is used.
                # Note that we only do this for method descriptors for now, we might want to
                # extend this to any descriptor in the future (by simply checking for
                # `hasattr(assigned_value.default, '__get__')`).
                default = assigned_value.default.__get__(None, cls)
                assigned_value.default = default
                assigned_value._attributes_set['default'] = default

            field_info = FieldInfo_.from_annotated_attribute(ann_type, assigned_value, _source=AnnotationSource.CLASS)

            # Store the original annotation and assignment value that could be used to rebuild the field info later.
            field_info._original_assignment = assigned_value
            field_info._original_annotation = ann_type
            if not evaluated:
                field_info._complete = False
            elif 'final' in field_info._qualifiers and not field_info.is_required():
                warnings.warn(
                    f'Annotation {ann_name!r} is marked as final and has a default value. Pydantic treats {ann_name!r} as a '
                    'class variable, but it will be considered as a normal field in V3 to be aligned with dataclasses. If you '
                    f'still want {ann_name!r} to be considered as a class variable, annotate it as: `ClassVar[<type>] = <default>.`',
                    category=PydanticDeprecatedSince211,
                    # Incorrect when `create_model` is used, but the chance that final with a default is used is low in that case:
                    stacklevel=4,
                )
                class_vars.add(ann_name)
                continue

            # attributes which are fields are removed from the class namespace:
            # 1. To match the behaviour of annotation-only fields
            # 2. To avoid false positives in the NameError check above
            try:
                delattr(cls, ann_name)
            except AttributeError:
                pass  # indicates the attribute was on a parent class

        # Use cls.__dict__['__pydantic_decorators__'] instead of cls.__pydantic_decorators__
        # to make sure the decorators have already been built for this exact class
        decorators: DecoratorInfos = cls.__dict__['__pydantic_decorators__']
        if ann_name in decorators.computed_fields:
            raise TypeError(
                f'Field {ann_name!r} of class {cls.__name__!r} overrides symbol of same name in a parent class. '
                'This override with a computed_field is incompatible.'
            )
        fields[ann_name] = field_info

        if field_info._complete:
            # If not complete, this will be called in `rebuild_model_fields()`:
            update_field_from_config(config_wrapper, ann_name, field_info)

    if config_wrapper.use_attribute_docstrings:
        _update_fields_from_docstrings(cls, fields)

    pydantic_extra_info: PydanticExtraInfo | None = None
    if '__pydantic_extra__' in type_hints:
        ann, complete = type_hints['__pydantic_extra__']
        pydantic_extra_info = PydanticExtraInfo(
            annotation=ann,
            complete=complete,
        )

    return fields, pydantic_extra_info, class_vars

