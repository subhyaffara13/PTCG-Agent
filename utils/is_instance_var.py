
def is_instance_var(var: Var) -> bool:
    """Return if var is an instance variable according to PEP 526."""
    return (
        # check the type_info node is the var (not a decorated function, etc.)
        var.name in var.info.names
        and var.info.names[var.name].node is var
        and not var.is_classvar
        # variables without annotations are treated as classvar
        and not var.is_inferred
    )

