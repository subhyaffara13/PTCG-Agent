
def my_script_ref_add(ref_t1: RRef[torch.Tensor], t2: torch.Tensor) -> torch.Tensor:
    t1 = ref_t1.to_here()
    return torch.add(t1, t2)

