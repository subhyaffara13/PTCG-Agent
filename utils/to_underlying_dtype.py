
def to_underlying_dtype(qdtype):
    DTYPE_MAPPING = {
        torch.quint8: torch.uint8,
        torch.qint8: torch.int8,
        torch.qint32: torch.int32,
        torch.quint4x2: torch.uint8,
        torch.quint2x4: torch.uint8,
        torch.uint8: torch.uint8,
        torch.int8: torch.int8,
        torch.uint16: torch.uint16,
        torch.int16: torch.int16,
        torch.int32: torch.int32,
        torch.float8_e5m2: torch.float8_e5m2,
        torch.float8_e4m3fn: torch.float8_e4m3fn,
    }
    if qdtype not in DTYPE_MAPPING:
        raise AssertionError("Unsupported dtype: " + str(qdtype))
    return DTYPE_MAPPING[qdtype]

