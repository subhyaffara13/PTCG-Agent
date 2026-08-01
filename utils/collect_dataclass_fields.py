
def collect_dataclass_fields(
    cls: type[StandardDataclass],
    *,
    config_wrapper: ConfigWrapper,
    ns_resolver: NsResolver | None = None,
    typevars_map: dict[Any, Any] | None = None,
) -> dict[str, FieldInfo]:
    """Collect the fields of a dataclass.

    Args:
        cls: dataclass.
        config_wrapper: The config wrapper instance.
        ns_resolver: Namespace resolver to use when getting dataclass annotations.
            Defaults to an empty instance.
        typevars_map: A dictionary mapping type variables to their concrete types.

    Returns:
        The dataclass fields.
    """
    FieldInfo_ = import_cached_field_info()

    fields: dict[str, FieldInfo] = {}
    ns_resolver = ns_resolver or NsResolver()
    dataclass_fields = cls.__dataclass_fields__

    # The logic here is similar to `_typing_extra.get_cls_type_hints`,
    # although we do it manually as stdlib dataclasses already have annotations
    # collected in each class:
    for base in reversed(cls.__mro__):
        if not dataclasses.is_dataclass(base):
            continue

        with ns_resolver.push(base):
            for ann_name, dataclass_field in dataclass_fields.items():
                base_anns = _typing_extra.safe_get_annotations(base)

                if ann_name not in base_anns:
                    # `__dataclass_fields__`contains every field, even the ones from base classes.
                    # Only collect the ones defined on `base`.
                    continue

                globalns, localns = ns_resolver.types_namespace
                ann_type, evaluated = _typing_extra.try_eval_type(dataclass_field.type, globalns, localns)

                if _typing_extra.is_classvar_annotation(ann_type):
                    continue

                if (
                    not dataclass_field.init
                    and dataclass_field.default is dataclasses.MISSING
                    and dataclass_field.default_factory is dataclasses.MISSING
                ):
                    # TODO: We should probably do something with this so that validate_assignment behaves properly
                    #   Issue: https://github.com/pydantic/pydantic/issues/5470
                    continue

                if isinstance(dataclass_field.default, FieldInfo_):
                    if dataclass_field.default.init_var:
                        if dataclass_field.default.init is False:
                            raise PydanticUserError(
                                f'Dataclass field {ann_name} has init=False and init_var=True, but these are mutually exclusive.',
                                code='clashing-init-and-init-var',
                            )

                        # TODO: same note as above re validate_assignment
                        continue
                    field_info = FieldInfo_.from_annotated_attribute(
                        ann_type, dataclass_field.default, _source=AnnotationSource.DATACLASS
                    )
                    field_info._original_assignment = dataclass_field.default
                else:
                    field_info = FieldInfo_.from_annotated_attribute(
                        ann_type, dataclass_field, _source=AnnotationSource.DATACLASS
                    )
                    field_info._original_assignment = dataclass_field

                if not evaluated:
                    field_info._complete = False
                    field_info._original_annotation = ann_type

                fields[ann_name] = field_info
                update_field_from_config(config_wrapper, ann_name, field_info)

                if field_info.default is not PydanticUndefined and isinstance(
                    getattr(cls, ann_name, field_info), FieldInfo_
                ):
                    # We need this to fix the default when the "default" from __dataclass_fields__ is a pydantic.FieldInfo
                    setattr(cls, ann_name, field_info.default)

    if typevars_map:
        for field in fields.values():
            # We don't pass any ns, as `field.annotation`
            # was already evaluated. TODO: is this method relevant?
            # Can't we juste use `_generics.replace_types`?
            field.apply_typevars_map(typevars_map)

    if config_wrapper.use_attribute_docstrings:
        _update_fields_from_docstrings(
            cls,
            fields,
            # We can't rely on the (more reliable) frame inspection method
            # for stdlib dataclasses:
            use_inspect=not hasattr(cls, '__is_pydantic_dataclass__'),
        )

    return fields

