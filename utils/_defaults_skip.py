
def _defaults_skip(stmt: AssignmentStmt, cls_type: str | None) -> bool:
    """Whether a class-level default assignment is skipped when emitting
    __mypyc_defaults_setup, based on class type.

    - attr (auto_attribs=False): skip all (handled by attr.ib machinery).
    - dataclasses / attr-auto: skip annotated assignments.
    - regular extension class: skip nothing.
    """
    if cls_type == "attr":
        return True
    if cls_type in ("dataclasses", "attr-auto"):
        return stmt.type is not None
    return False

