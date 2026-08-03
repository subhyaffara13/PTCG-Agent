from typing import Any

def bytes_to_scalar(byte_list: list[int], dtype: torch.dtype, device: torch.device):
    dtype_to_ctype: dict[torch.dtype, Any] = {
        torch.int8: ctypes.c_int8,
        torch.uint8: ctypes.c_uint8,
        torch.uint16: ctypes.c_uint16,
        torch.uint32: ctypes.c_uint32,
        torch.uint64: ctypes.c_uint64,
        torch.int16: ctypes.c_int16,
        torch.int32: ctypes.c_int32,
        torch.int64: ctypes.c_int64,
        torch.bool: ctypes.c_bool,
        torch.float32: ctypes.c_float,
        torch.complex64: ctypes.c_float,
        torch.float64: ctypes.c_double,
        torch.complex128: ctypes.c_double,
    }
    ctype = dtype_to_ctype[dtype]
    num_bytes = ctypes.sizeof(ctype)

    def check_bytes(byte_list):
        for byte in byte_list:
            if not (0 <= byte <= 255):
                raise AssertionError(f"byte value out of range: expected 0 <= byte <= 255, got {byte}")

    if dtype.is_complex:
        if len(byte_list) != (num_bytes * 2):
            raise AssertionError(
                f"expected len(byte_list) == {num_bytes * 2} for complex dtype, got {len(byte_list)}"
            )
        check_bytes(byte_list)
        real = ctype.from_buffer((ctypes.c_byte * num_bytes)(
            *byte_list[:num_bytes])).value
        imag = ctype.from_buffer((ctypes.c_byte * num_bytes)(
            *byte_list[num_bytes:])).value
        res = real + 1j * imag
    else:
        if len(byte_list) != num_bytes:
            raise AssertionError(
                f"expected len(byte_list) == {num_bytes}, got {len(byte_list)}"
            )
        check_bytes(byte_list)
        res = ctype.from_buffer((ctypes.c_byte * num_bytes)(
            *byte_list)).value

    return torch.tensor(res, device=device, dtype=dtype)

