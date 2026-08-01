
def dt_fmt():
    from sys import byteorder

    e = "<" if byteorder == "little" else ">"
    return (
        "{{'names':['bool_','uint_','float_','ldbl_'],"
        "'formats':['?','" + e + "u4','" + e + "f4','" + e + "f{}'],"
        "'offsets':[0,4,8,{}],'itemsize':{}}}"
    )

