
def save_rref(rref_var: RRef[Tensor], fname: str) -> None:
    torch.save(rref_var, fname)

