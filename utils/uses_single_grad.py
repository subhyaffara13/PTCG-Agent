
def uses_single_grad(info: DifferentiabilityInfo | None) -> bool:
    return uses_ident(info, "grad")

