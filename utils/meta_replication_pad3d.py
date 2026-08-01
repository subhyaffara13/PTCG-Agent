
def meta_replication_pad3d(input, padding):
    torch._check(
        input.dtype != torch.bool,
        lambda: f""""replication_pad3d" not implemented for '{input.dtype.__str__()}'""",
    )
    return _pad3d_common(input, padding, is_reflection=False)

