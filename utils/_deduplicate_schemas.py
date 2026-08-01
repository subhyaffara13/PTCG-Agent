
def _deduplicate_schemas(schemas: Iterable[JsonDict]) -> list[JsonDict]:
    return list({_make_json_hashable(schema): schema for schema in schemas}.values())

