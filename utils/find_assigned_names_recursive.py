
def find_assigned_names_recursive(
    target: nodes.AssignName | nodes.BaseContainer,
) -> Iterator[str]:
    """Yield the names of assignment targets, accounting for nested ones."""
    match target:
        case nodes.AssignName():
            if target.name is not None:
                yield target.name
        case nodes.BaseContainer():
            for elt in target.elts:
                yield from find_assigned_names_recursive(elt)

