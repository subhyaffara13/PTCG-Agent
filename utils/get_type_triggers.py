
def get_type_triggers(
    typ: Type, use_logical_deps: bool, seen_aliases: set[TypeAliasType] | None = None
) -> list[str]:
    """Return all triggers that correspond to a type becoming stale."""
    return typ.accept(TypeTriggersVisitor(use_logical_deps, seen_aliases))

