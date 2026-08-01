
def _lowercase_labels(ops):
    if not isinstance(ops, set):
        ops = [ops]

    return [str(arg.label[0]).lower() for arg in ops]

