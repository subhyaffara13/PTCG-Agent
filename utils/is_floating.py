
def is_floating(x):
    return promote_to_tensor(x).dtype.is_floating()

