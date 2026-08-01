
def number_type(
    x: NumberType | torch.SymInt | torch.SymFloat | torch.SymBool,
) -> type:
    if isinstance(x, torch.SymInt):
        return int
    elif isinstance(x, torch.SymFloat):
        return float
    elif isinstance(x, torch.SymBool):
        return bool
    else:
        return type(x)

