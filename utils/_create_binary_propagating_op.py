
def _create_binary_propagating_op(name, is_divmod=False):
    is_cmp = name.strip("_") in ["eq", "ne", "le", "lt", "ge", "gt"]

    def method(self, other):
        if (
            other is pd_NA
            or isinstance(other, (str, bytes, numbers.Number, np.bool))
            or (isinstance(other, np.ndarray) and not other.shape)
        ):
            # Need the other.shape clause to handle NumPy scalars,
            # since we do a setitem on `out` below, which
            # won't work for NumPy scalars.
            if is_divmod:
                return pd_NA, pd_NA
            else:
                return pd_NA

        elif isinstance(other, np.ndarray):
            out = np.empty(other.shape, dtype=object)
            out[:] = pd_NA

            if is_divmod:
                return out, out.copy()
            else:
                return out

        elif is_cmp and isinstance(other, (np.datetime64, np.timedelta64)):
            return pd_NA

        elif isinstance(other, np.datetime64):
            if name in ["__sub__", "__rsub__"]:
                return pd_NA

        elif isinstance(other, np.timedelta64):
            if name in ["__sub__", "__rsub__", "__add__", "__radd__"]:
                return pd_NA

        return NotImplemented

    method.__name__ = name
    return method

