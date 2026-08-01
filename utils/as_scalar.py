
def as_scalar(x):
    if type(x) is list:
        assert len(x) == 1
        return x[0]
    elif type(x) is np.ndarray:
        return x.item()
    else:
        return x

