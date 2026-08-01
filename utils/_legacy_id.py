
def _legacy_id(contents: ObjectSchema) -> URI | None:
    if "$ref" in contents:
        return
    id = contents.get("id")
    if id is not None and not id.startswith("#"):
        return id

