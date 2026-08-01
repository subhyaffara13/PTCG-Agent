
def count_eqns(
    jaxpr: core.Jaxpr, revisit_inner_jaxprs: bool = True
) -> int:
  return sum(1 for _ in all_eqns(jaxpr, revisit_inner_jaxprs=revisit_inner_jaxprs))

