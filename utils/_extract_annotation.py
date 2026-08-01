
def _extract_annotation(
    metadata: tuple, field_name: str
) -> declarative_asn1.Annotation:
    default = None
    encoding = None
    size = None
    for raw_annotation in metadata:
        if isinstance(raw_annotation, Default):
            if default is not None:
                raise TypeError(
                    f"multiple DEFAULT annotations found in field "
                    f"'{field_name}'"
                )
            default = raw_annotation.value
        elif isinstance(raw_annotation, declarative_asn1.Encoding):
            if encoding is not None:
                raise TypeError(
                    f"multiple IMPLICIT/EXPLICIT annotations found in field "
                    f"'{field_name}'"
                )
            encoding = raw_annotation
        elif isinstance(raw_annotation, declarative_asn1.Size):
            if size is not None:
                raise TypeError(
                    f"multiple SIZE annotations found in field '{field_name}'"
                )
            size = raw_annotation
        else:
            raise TypeError(f"unsupported annotation: {raw_annotation}")

    return declarative_asn1.Annotation(
        default=default, encoding=encoding, size=size
    )

