
def _get_precision_dict() -> dict[str, str]:
    names = [
        ("_NBitByte", np.byte),
        ("_NBitShort", np.short),
        ("_NBitIntC", np.intc),
        ("_NBitIntP", np.intp),
        ("_NBitInt", np.int_),
        ("_NBitLong", np.long),
        ("_NBitLongLong", np.longlong),

        ("_NBitHalf", np.half),
        ("_NBitSingle", np.single),
        ("_NBitDouble", np.double),
        ("_NBitLongDouble", np.longdouble),
    ]
    ret: dict[str, str] = {}
    for name, typ in names:
        n = 8 * np.dtype(typ).itemsize
        ret[f"{_MODULE}._nbit.{name}"] = f"{_MODULE}._nbit_base._{n}Bit"
    return ret

