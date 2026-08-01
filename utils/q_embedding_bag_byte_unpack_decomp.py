
def q_embedding_bag_byte_unpack_decomp(packed: torch.Tensor) -> torch.Tensor:
    def bitcast_u8_to_f32(u8: torch.Tensor) -> torch.Tensor:
        x, y, z, w = (u8[..., n].to(torch.int32) for n in (0, 1, 2, 3))
        if sys.byteorder == "little":
            return (x + (y << 8) + (z << 16) + (w << 24)).view(torch.float32)[..., None]
        else:
            return ((x << 24) + (y << 16) + (z << 8) + w).view(torch.float32)[..., None]

    scales = bitcast_u8_to_f32(packed[..., -8:-4])
    offsets = bitcast_u8_to_f32(packed[..., -4:])
    return packed[..., :-8].to(torch.float32) * scales + offsets

