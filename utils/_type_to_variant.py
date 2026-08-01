
def _type_to_variant(
    t: typing.Any, field_name: str
) -> declarative_asn1.Variant:
    is_annotated = typing.get_origin(t) is typing.Annotated
    inner_type = typing.get_args(t)[0] if is_annotated else t

    # Check if this is a Variant[T, Tag] type
    if typing.get_origin(inner_type) is Variant:
        value_type, tag_literal = typing.get_args(inner_type)
        if typing.get_origin(tag_literal) is not typing.Literal:
            raise TypeError(
                "When using `asn1.Variant` in a type annotation, the second "
                "type parameter must be a `typing.Literal` type. E.g: "
                '`Variant[int, typing.Literal["MyInt"]]`.'
            )
        tag_name = typing.get_args(tag_literal)[0]

        if hasattr(value_type, "__asn1_root__"):
            rust_type = value_type.__asn1_root__
        else:
            rust_type = declarative_asn1.non_root_python_to_rust(value_type)

        if is_annotated:
            ann_type = declarative_asn1.AnnotatedType(
                rust_type,
                _extract_annotation(t.__metadata__, field_name),
            )
        else:
            ann_type = declarative_asn1.AnnotatedType(
                rust_type,
                declarative_asn1.Annotation(),
            )

        return declarative_asn1.Variant(Variant, ann_type, tag_name)
    else:
        # Plain type (not a tagged Variant)
        return declarative_asn1.Variant(
            inner_type,
            _normalize_field_type(t, field_name),
            None,
        )

