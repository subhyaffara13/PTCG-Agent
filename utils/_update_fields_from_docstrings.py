
def _update_fields_from_docstrings(cls: type[Any], fields: dict[str, FieldInfo], use_inspect: bool = False) -> None:
    fields_docs = extract_docstrings_from_cls(cls, use_inspect=use_inspect)
    for ann_name, field_info in fields.items():
        if field_info.description is None and ann_name in fields_docs:
            field_info.description = fields_docs[ann_name]

