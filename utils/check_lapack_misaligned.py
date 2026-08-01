
def check_lapack_misaligned(func, args, kwargs):
    args = list(args)
    for i in range(len(args)):
        a = args[:]
        if isinstance(a[i], np.ndarray):
            # Try misaligning a[i]
            aa = np.zeros(a[i].size*a[i].dtype.itemsize+8, dtype=np.uint8)
            aa = np.frombuffer(aa.data, offset=4, count=a[i].size,
                               dtype=a[i].dtype)
            aa = aa.reshape(a[i].shape)
            aa[...] = a[i]
            a[i] = aa
            func(*a, **kwargs)
            if len(a[i].shape) > 1:
                a[i] = a[i].T
                func(*a, **kwargs)

