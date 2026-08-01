
def value_to_literal(value):
    if isinstance(value, str):
        # Quotes string and escapes special characters
        return ascii(value)
    if isinstance(value, torch.Tensor):
        return 'torch.' + str(value)
    else:
        return str(value)

