
def kwargs_of(node):
    kwargs = {}
    for attr in node.attribute:
        (key, value) = _attribute_to_pair(attr)
        kwargs.update({key: value})
    if node.domain:
        kwargs.update({"domain": node.domain})
    return kwargs

