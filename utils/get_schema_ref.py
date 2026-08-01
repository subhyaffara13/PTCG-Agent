
def get_schema_ref(name: str, ref_prefix: Optional[str], ref_template: str, schema_overrides: bool) -> Dict[str, Any]:
    if ref_prefix:
        schema_ref = {'$ref': ref_prefix + name}
    else:
        schema_ref = {'$ref': ref_template.format(model=name)}
    return {'allOf': [schema_ref]} if schema_overrides else schema_ref

