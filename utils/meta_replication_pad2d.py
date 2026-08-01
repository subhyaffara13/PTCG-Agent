
def meta_replication_pad2d(input, padding):
    torch._check(
        input.dtype != torch.bool,
        lambda: f""""replication_pad2d" not implemented for '{input.dtype.__str__()}'""",
    )
    return _pad2d_common(input, padding, is_reflection=False)

