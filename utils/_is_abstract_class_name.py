
def _is_abstract_class_name(name: str) -> bool:
    lname = name.lower()
    is_mixin = lname.endswith("mixin")
    is_abstract = lname.startswith("abstract")
    is_base = lname.startswith("base") or lname.endswith("base")
    return is_mixin or is_abstract or is_base

