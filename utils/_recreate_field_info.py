from typing import Any

def _recreate_field_info(
    field_info: FieldInfo,
    ns_resolver: NsResolver,
    typevars_map: Mapping[TypeVar, Any],
    *,
    lenient: bool,
) -> FieldInfo:
    FieldInfo_ = import_cached_field_info()

    existing_desc = field_info.description
    if lenient:
        ann = _generics.replace_types(field_info._original_annotation, typevars_map)
        ann, evaluated = _typing_extra.try_eval_type(
            ann,
            *ns_resolver.types_namespace,
        )
    else:
        # Not the best pattern, maybe we could ship our own `eval_type()`,
        # that would replace the type variables on the fly during evaluation.
        ann = _typing_extra.eval_type(
            field_info._original_annotation,
            *ns_resolver.types_namespace,
        )
        ann = _generics.replace_types(ann, typevars_map)
        ann = _typing_extra.eval_type(
            ann,
            *ns_resolver.types_namespace,
        )
        evaluated = True

    if (assign := field_info._original_assignment) is PydanticUndefined:
        new_field = FieldInfo_.from_annotation(ann, _source=AnnotationSource.CLASS)
    else:
        new_field = FieldInfo_.from_annotated_attribute(ann, assign, _source=AnnotationSource.CLASS)
        new_field._original_assignment = assign
    new_field._original_annotation = ann
    # The description might come from the docstring if `use_attribute_docstrings` was `True`:
    new_field.description = new_field.description if new_field.description is not None else existing_desc
    if not evaluated:
        new_field._complete = False

    return new_field

