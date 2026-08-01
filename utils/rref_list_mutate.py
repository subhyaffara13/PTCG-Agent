
def rref_list_mutate(rref: RRef[list[int]]) -> None:
    rref.local_value().append(4)
    rref.to_here().append(5)
    rref.to_here(5.0).append(6)

