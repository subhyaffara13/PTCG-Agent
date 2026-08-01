
def _set_metadata_attributes(span: "Span", metadata: Optional[Any], span_attrs) -> None:
    if metadata is not None:
        safe_set_attribute(span, span_attrs.METADATA, safe_dumps(metadata))

