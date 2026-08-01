
def arr_obj(
    arr_float, arr_int, arr_bool, arr_complex, arr_str, arr_utf, arr_date, arr_tdelta
):
    return np.vstack(
        [
            arr_float.astype("O"),
            arr_int.astype("O"),
            arr_bool.astype("O"),
            arr_complex.astype("O"),
            arr_str.astype("O"),
            arr_utf.astype("O"),
            arr_date.astype("O"),
            arr_tdelta.astype("O"),
        ]
    )

