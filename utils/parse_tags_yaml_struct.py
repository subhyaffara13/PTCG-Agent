
def parse_tags_yaml_struct(es: object, path: str = "<stdin>") -> set[str]:
    if not isinstance(es, list):
        raise AssertionError(f"Expected 'es' to be a list, but got {type(es)}")
    rs: set[str] = set()
    for e in es:
        if not isinstance(e.get("__line__"), int):
            raise AssertionError(f"Expected '__line__' to be int: {e}")
        loc = Location(path, e["__line__"])
        tags = e.get("tag")
        with context(lambda: f"in {loc}:\n  {tags}"):
            e_i = e.copy()
            name = e_i.pop("tag")
            desc = e_i.pop("desc", "")
            # ensure that each tag has a non-empty description
            if desc == "":
                raise AssertionError(f"Tag '{name}' must have a non-empty description")
            rs.add(name)
    return rs

