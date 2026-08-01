
def _make_dict_items(obj, is_ordered=False):
    if is_ordered:
        return OrderedDict(obj).items()
    else:
        return obj.items()

