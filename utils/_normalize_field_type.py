
def _normalize_field_type(
    field_type: typing.Any, field_name: str
) -> declarative_asn1.AnnotatedType:
    field_type = _resolve_type_aliases(field_type)

    # Strip the `Annotated[...]` off, and populate the annotation
    # from it if it exists.
    if typing.get_origin(field_type) is typing.Annotated:
        annotation = _extract_annotation(field_type.__metadata__, field_name)
        field_type, *_ = typing.get_args(field_type)
    else:
        annotation = declarative_asn1.Annotation()

    if annotation.size is not None and (
        typing.get_origin(field_type) not in (builtins.list, SetOf)
        and field_type
        not in (
            builtins.bytes,
            builtins.str,
            BitString,
            IA5String,
            PrintableString,
        )
    ):
        raise TypeError(
            f"field '{field_name}' has a SIZE annotation, but SIZE "
            "annotations are only supported for fields of types: "
            "[SEQUENCE OF, SET OF, BIT STRING, OCTET STRING, UTF8String, "
            "PrintableString, IA5String]"
        )

    if field_type is TLV:
        if isinstance(annotation.encoding, Implicit):
            raise TypeError(
                f"field '{field_name}' has an IMPLICIT annotation, but "
                "IMPLICIT annotations are not supported for TLV types."
            )
        elif annotation.default is not None:
            raise TypeError(
                f"field '{field_name}' has a DEFAULT annotation, but "
                "DEFAULT annotations are not supported for TLV types."
            )

    _check_x509_field_annotations(field_type, annotation, field_name)

    if hasattr(field_type, "__asn1_root__"):
        root_type = field_type.__asn1_root__
        if not isinstance(
            root_type,
            (
                declarative_asn1.Type.Sequence,
                declarative_asn1.Type.Set,
                declarative_asn1.Type.ValueSet,
            ),
        ):
            raise TypeError(f"unsupported root type: {root_type}")
        return declarative_asn1.AnnotatedType(
            typing.cast(declarative_asn1.Type, root_type), annotation
        )
    elif _is_union(field_type):
        union_args = typing.get_args(field_type)
        if len(union_args) == 2 and NoneType in union_args:
            # A Union between a type and None is an OPTIONAL
            optional_type = (
                union_args[0] if union_args[1] is type(None) else union_args[1]
            )
            if optional_type is TLV:
                raise TypeError(
                    "optional TLV types (`TLV | None`) are not "
                    "currently supported"
                )
            # For optional types, the annotation is associated with the
            # union, so we check it against the inner type here.
            _check_x509_field_annotations(
                optional_type, annotation, field_name
            )
            annotated_type = _normalize_field_type(optional_type, field_name)

            if not annotated_type.annotation.is_empty():
                raise TypeError(
                    "optional (`X | None`) types cannot have `X` "
                    "annotated: annotations must apply to the union "
                    "(i.e: `Annotated[X | None, annotation]`)"
                )

            if annotation.default is not None:
                raise TypeError(
                    "optional (`X | None`) types should not have a DEFAULT "
                    "annotation"
                )

            rust_field_type = declarative_asn1.Type.Option(annotated_type)

        else:
            # Otherwise, the Union is a CHOICE
            if isinstance(annotation.encoding, Implicit):
                # CHOICEs cannot be IMPLICIT. See X.680 section 31.2.9.
                raise TypeError(
                    "CHOICE (`X | Y | ...`) types should not have an IMPLICIT "
                    "annotation"
                )
            variants = [
                _type_to_variant(arg, field_name)
                for arg in union_args
                if arg is not type(None)
            ]

            # Union types should either be all Variants
            # (`Variant[..] | Variant[..] | etc`) or all non Variants
            are_union_types_tagged = variants[0].tag_name is not None
            if any(
                (v.tag_name is not None) != are_union_types_tagged
                for v in variants
            ):
                raise TypeError(
                    "When using `asn1.Variant` in a union, all the other "
                    "types in the union must also be `asn1.Variant`"
                )

            if are_union_types_tagged:
                tags = {v.tag_name for v in variants}
                if len(variants) != len(tags):
                    raise TypeError(
                        "When using `asn1.Variant` in a union, the tags used "
                        "must be unique"
                    )

            rust_choice_type = declarative_asn1.Type.Choice(variants)
            # If None is part of the union types, this is an OPTIONAL CHOICE
            rust_field_type = (
                declarative_asn1.Type.Option(
                    declarative_asn1.AnnotatedType(
                        rust_choice_type, declarative_asn1.Annotation()
                    )
                )
                if NoneType in union_args
                else rust_choice_type
            )

    elif typing.get_origin(field_type) is builtins.list:
        inner_type = _normalize_field_type(
            typing.get_args(field_type)[0], field_name
        )
        rust_field_type = declarative_asn1.Type.SequenceOf(inner_type)
    elif typing.get_origin(field_type) is SetOf:
        inner_type = _normalize_field_type(
            typing.get_args(field_type)[0], field_name
        )
        rust_field_type = declarative_asn1.Type.SetOf(inner_type)
    else:
        rust_field_type = declarative_asn1.non_root_python_to_rust(field_type)

    return declarative_asn1.AnnotatedType(rust_field_type, annotation)

