
def _replace_values_in_tensor(tensor, condition, safe_value):
    mask = condition(tensor)
    tensor.masked_fill_(mask, safe_value)

