from typing import Any

def partition_pvals(
    pvals: list[PartialVal]
  ) -> tuple[list[bool], list[AbstractValue], list[Any]]:
  knowns = [pval.is_known()  for pval in pvals                       ]
  avals  = [pval.get_aval()  for pval in pvals if not pval.is_known()]
  consts = [pval.get_known() for pval in pvals if     pval.is_known()]
  return knowns, avals, consts

