
def uses_retain_variables(info: DifferentiabilityInfo | None) -> bool:
    return uses_ident(info, "retain_variables")

