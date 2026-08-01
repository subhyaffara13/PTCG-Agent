
def numeric_as_float(data):
    for v in data.columns:
        if data[v].dtype is np.dtype("int64"):
            data[v] = data[v].astype(np.float64)

