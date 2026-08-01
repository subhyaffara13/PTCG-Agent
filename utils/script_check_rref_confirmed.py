
def script_check_rref_confirmed(rref: RRef[Tensor]) -> bool:
    return rref.confirmed_by_owner()

