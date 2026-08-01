
def _dtype_to_storage_type_map():
    # NOTE: We should no longer add dtypes to this map. This map
    # is only used for BC/FC with older PyTorch versions. Going forward,
    # new dtypes of TypedStorage should not translate to a legacy
    # <type>Storage class. Instead, new dtypes of TypedStorage should
    # be serialized as an UntypedStorage paired with a torch.dtype
    return {
        torch.double: "DoubleStorage",
        torch.float: "FloatStorage",
        torch.half: "HalfStorage",
        torch.long: "LongStorage",
        torch.int: "IntStorage",
        torch.int16: "ShortStorage",
        torch.int8: "CharStorage",
        torch.uint8: "ByteStorage",
        torch.bool: "BoolStorage",
        torch.bfloat16: "BFloat16Storage",
        torch.cdouble: "ComplexDoubleStorage",
        torch.cfloat: "ComplexFloatStorage",
        torch.qint8: "QInt8Storage",
        torch.qint32: "QInt32Storage",
        torch.quint8: "QUInt8Storage",
        torch.quint4x2: "QUInt4x2Storage",
        torch.quint2x4: "QUInt2x4Storage",
    }

