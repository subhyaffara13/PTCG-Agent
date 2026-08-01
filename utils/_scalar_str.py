
def _scalar_str(self, formatter1, formatter2=None):
    if formatter2 is not None:
        real_str = _scalar_str(self.real, formatter1)
        imag_str = (_scalar_str(self.imag, formatter2) + "j").lstrip()
        # handles negative numbers, +0.0, -0.0
        if imag_str[0] == "+" or imag_str[0] == "-":
            return real_str + imag_str
        else:
            return real_str + "+" + imag_str
    else:
        return formatter1.format(self.item())


def _scalar_str(dtype, short):
    byteorder = _byte_order_str(dtype)

    if dtype.type == np.bool:
        if short:
            return "'?'"
        else:
            return "'bool'"

    elif dtype.type == np.object_:
        # The object reference may be different sizes on different
        # platforms, so it should never include the itemsize here.
        return "'O'"

    elif dtype.type == np.bytes_:
        if _isunsized(dtype):
            return "'S'"
        else:
            return f"'S{dtype.itemsize}'"

    elif dtype.type == np.str_:
        if _isunsized(dtype):
            return f"'{byteorder}U'"
        else:
            return f"'{byteorder}U{dtype.itemsize // 4}'"

    elif dtype.type is str:
        return "'T'"

    elif not type(dtype)._legacy:
        return f"'{byteorder}{type(dtype).__name__}{dtype.itemsize * 8}'"

    # unlike the other types, subclasses of void are preserved - but
    # historically the repr does not actually reveal the subclass
    elif issubclass(dtype.type, np.void):
        if _isunsized(dtype):
            return "'V'"
        else:
            return f"'V{dtype.itemsize}'"

    elif dtype.type == np.datetime64:
        return f"'{byteorder}M8{_datetime_metadata_str(dtype)}'"

    elif dtype.type == np.timedelta64:
        return f"'{byteorder}m8{_datetime_metadata_str(dtype)}'"

    elif dtype.isbuiltin == 2:
        return dtype.type.__name__

    elif np.issubdtype(dtype, np.number):
        # Short repr with endianness, like '<f8'
        if short or dtype.byteorder not in ('=', '|'):
            return f"'{byteorder}{dtype.kind}{dtype.itemsize}'"

        # Longer repr, like 'float64'
        else:
            return f"'{_kind_name(dtype)}{8 * dtype.itemsize}'"

    else:
        raise RuntimeError(
            "Internal error: NumPy dtype unrecognized type number")

