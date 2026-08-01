
def packed_dtype_fmt():
    from sys import byteorder

    return "[('bool_','?'),('uint_','{e}u4'),('float_','{e}f4'),('ldbl_','{e}f{}')]".format(
        np.dtype("longdouble").itemsize, e="<" if byteorder == "little" else ">"
    )

