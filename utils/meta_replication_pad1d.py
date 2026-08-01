
def meta_replication_pad1d(input, padding):
    torch._check(
        input.dtype != torch.bool,
        lambda: f""""replication_pad1d" not implemented for '{input.dtype.__str__()}'""",
    )
    return _pad1d_common(input, padding, is_reflection=False)

