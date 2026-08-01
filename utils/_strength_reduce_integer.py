
def _strength_reduce_integer(val: int) -> torch.dtype:
    for possible_dtype in (torch.uint8, torch.uint16, torch.int32):
        if val <= torch.iinfo(possible_dtype).max:
            return possible_dtype
    return torch.int64

