
def convert_element_type_noop(x, dtype: torch.dtype):
    return x.dtype == dtype

