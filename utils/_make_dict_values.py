
def _make_dict_values(obj, is_ordered=False):
    if is_ordered:
        return OrderedDict((i, _) for i, _ in enumerate(obj)).values()
    else:
        return {i: _ for i, _ in enumerate(obj)}.values()

