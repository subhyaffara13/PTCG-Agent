
def buffer_length(arr):
    if isinstance(arr, str):
        if not arr:
            charmax = 0
        else:
            charmax = max(ord(c) for c in arr)
        if charmax < 256:
            size = 1
        elif charmax < 65536:
            size = 2
        else:
            size = 4
        return size * len(arr)
    v = memoryview(arr)
    if v.shape is None:
        return len(v) * v.itemsize
    else:
        return np.prod(v.shape) * v.itemsize

