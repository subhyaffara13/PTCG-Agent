
def repr_format(x):
    if isinstance(x, (np.str_, np.bytes_)):
        return repr(x.item())
    return repr(x)

