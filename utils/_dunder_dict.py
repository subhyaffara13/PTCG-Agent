
def _dunder_dict(instance, attributes):
    obj = node_classes.Dict(
        parent=instance,
        lineno=instance.lineno,
        col_offset=instance.col_offset,
        end_lineno=instance.end_lineno,
        end_col_offset=instance.end_col_offset,
    )

    # Convert the keys to node strings
    keys = [
        node_classes.Const(value=value, parent=obj) for value in list(attributes.keys())
    ]

    # The original attribute has a list of elements for each key,
    # but that is not useful for retrieving the special attribute's value.
    # In this case, we're picking the last value from each list.
    values = [elem[-1] for elem in attributes.values()]

    obj.postinit(list(zip(keys, values)))
    return obj

