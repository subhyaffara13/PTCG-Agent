
def _int_floor(arr, xp):
    # array_api_strict is strict about not allowing `int()` on a float array.
    # That's typically not needed, here it is - so explicitly convert
    return int(xp.asarray(arr, dtype=xp.int64))

