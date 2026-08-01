
def str_format(x):
    if isinstance(x, (np.str_, np.bytes_)):
        return str(x.item())
    return str(x)

