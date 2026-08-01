
def wrap_check_inputs(check_inputs):
    if check_inputs is None:
        return None

    return [{"forward": c} for c in check_inputs]

