
def rref_local_value(rref: RRef[Tensor]) -> Tensor:
    return rref.local_value()

