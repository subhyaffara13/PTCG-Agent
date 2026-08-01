
def enforce_list(variable):
    if isinstance(variable, list):
        return variable
    return [variable]

