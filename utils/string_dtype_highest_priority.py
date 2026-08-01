
def string_dtype_highest_priority(dtype1, dtype2):
    if HAS_PYARROW:
        DTYPE_HIERARCHY = [
            StringDtype("python", na_value=np.nan),
            StringDtype("pyarrow", na_value=np.nan),
            StringDtype("python", na_value=NA),
            StringDtype("pyarrow", na_value=NA),
        ]
    else:
        DTYPE_HIERARCHY = [
            StringDtype("python", na_value=np.nan),
            StringDtype("python", na_value=NA),
        ]

    h1 = DTYPE_HIERARCHY.index(dtype1)
    h2 = DTYPE_HIERARCHY.index(dtype2)
    return DTYPE_HIERARCHY[max(h1, h2)]

