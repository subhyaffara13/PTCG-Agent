
def _check_x509_field_annotations(
    field_type: typing.Any,
    annotation: declarative_asn1.Annotation,
    field_name: str,
) -> None:
    if field_type in _X509_TYPES and isinstance(annotation.encoding, Implicit):
        raise TypeError(
            f"field '{field_name}' has an IMPLICIT annotation, but "
            "IMPLICIT annotations are not supported for X.509 types."
        )

