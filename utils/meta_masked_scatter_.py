
def meta_masked_scatter_(self, mask, source):
    torch._check(
        mask.dtype in (torch.bool, torch.uint8), lambda: "Mask must be bool or uint8"
    )
    torch._check(
        self.dtype == source.dtype,
        lambda: "masked_scatter: expected self and source to have same "
        f"dtypes but got {self.dtype} and {source.dtype}",
    )
    return self

