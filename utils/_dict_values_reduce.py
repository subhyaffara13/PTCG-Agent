
def _dict_values_reduce(obj):
    # Safer not to ship the full dict as sending the rest might
    # be unintended and could potentially cause leaking of
    # sensitive information
    return _make_dict_values, (list(obj),)

