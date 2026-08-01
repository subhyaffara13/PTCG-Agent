
def rref_to_here_with_timeout(rref_var: RRef[Tensor], timeout: float) -> Tensor:
    return rref_var.to_here(timeout)

