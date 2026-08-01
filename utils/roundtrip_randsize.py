
def roundtrip_randsize(arr):
    f = BytesIO()
    format.write_array(f, arr)
    f2 = BytesIOSRandomSize(f.getvalue())
    arr2 = format.read_array(f2)
    return arr2

