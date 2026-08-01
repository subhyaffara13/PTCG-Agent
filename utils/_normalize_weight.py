
def _normalize_weight(weight):
    return weight if isinstance(weight, Integral) else weight_dict[weight]

