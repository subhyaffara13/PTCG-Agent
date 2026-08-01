
def _uppercase_labels(ops):
    if not isinstance(ops, set):
        ops = [ops]

    new_args = [str(arg.label[0])[0].upper() +
                str(arg.label[0])[1:] for arg in ops]

    return new_args

