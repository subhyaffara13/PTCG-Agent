
def roundtrip_truncated(arr):
    f = BytesIO()
    format.write_array(f, arr)
    # BytesIO is one byte short
    f2 = BytesIO(f.getvalue()[0:-1])
    arr2 = format.read_array(f2)
    return arr2

