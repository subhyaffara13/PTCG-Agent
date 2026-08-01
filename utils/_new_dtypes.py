
def _new_dtypes():
    # These are dtypes serialized as UntypedStorage unlike those in
    # _dtype_to_storage_type_map
    return {
        torch.float8_e5m2,
        torch.float8_e4m3fn,
        torch.float8_e5m2fnuz,
        torch.float8_e4m3fnuz,
        torch.float8_e8m0fnu,
        torch.float4_e2m1fn_x2,
        torch.bits8,
        torch.bits16,
        torch.bits1x8,
        torch.bits2x4,
        torch.bits4x2,
        torch.complex32,
        torch.uint16,
        torch.uint32,
        torch.uint64,
    }

